using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Management;
using HS.Dialogs;

namespace musicGuru
{
    public partial class RecordForm : Form
    {
        public RecordForm()
        {
            InitializeComponent();
            ManagementObject disk = new ManagementObject("win32_logicaldisk.deviceid=\"c:\""); 
            disk.Get();
            if (Program.App.PrepareBurning(Convert.ToUInt64(disk["FreeSpace"])))
            {
                int minMb = Program.App.MinimumFreeBytes / (1024 * 1024);
                int maxMb = Program.App.RecommendedFreeBytes / (1024 * 1024);
                lblRequiredSpace.Text = string.Format("Minimum: {0} MB Recommended: {1} MB", minMb, maxMb);
            }
            _FillCDList();
            _UpdateDevices();
        }

        private void _FillCDList()
        {
            lvCD.Items.Clear();
            foreach (Node node in Program.App.Board.Nodes)
            {
                if (node.IsContainer)
                {
                    ListViewItem lvi = lvCD.Items.Add(node.Name);
                    lvi.SubItems.Add(node.Songs);
                    lvi.SubItems.Add(node.Size);
                    lvi.Checked = true;
                    lvi.Tag = node;
                }
            }
        }

        private void _AddDir(StarBurn.CNode root, Node node)
        {
            foreach (Node subNode in node.Nodes)
            {
                if (subNode.IsContainer)
                {
                    StarBurn.CNode newRoot = root.CreateNewFolder(subNode.Name);
                    _AddDir(newRoot, subNode);
                }
                else
                    root.AddFile(subNode.Name, subNode.PhysicalPath);
            }
        }

        private bool _RecordNode(Node node)
        {
            StarBurn.CJolietImage jolietImage = new StarBurn.CJolietImage();
            _AddDir(jolietImage.Root, node);
            jolietImage.Build(0, node.Name, Application.ProductName);
            string msg = string.Format("The CD '{0}' is about to be recorded. Insert a blank CD/DVD and click OK.", node.Name);
            if (MessageBox.Show(msg, "Insert a blank CD", MessageBoxButtons.OKCancel) != DialogResult.OK)
                throw new RecodingAbortedException();
            int selectedIndex = cbDevices.SelectedIndex;
            if (selectedIndex < 0)
                selectedIndex = 0;
            StarBurn.CDevices devices = new StarBurn.CDevicesClass();
            if (devices.Count == 0)
            {
                MessageBox.Show("There is no device to record on.");
                throw new RecodingAbortedException();
            }
            StarBurn.CDevice device = devices.GetDevice(selectedIndex);
            if (!(device.SupportDVDPlusRWrite ||
                device.SupportDVDPlusRWWrite ||
                device.SupportDVDRAMWrite ||
                device.SupportDVDRWrite ||
                device.SupportCDRWrite ||
                device.SupportCDRWWrite))
            {
                MessageBox.Show("The selected device is not writable.", "Error");
                throw new RecodingAbortedException();
            }
            try
            {
                device.TestUnitReady();
            }
            catch
            {
                MessageBox.Show("Device isn't ready", "Error");
                return false;
            }
            StarBurn.CDiscInfo discInfo = device.GetDiscInfo();
            if (!discInfo.IsBlank)
            {
                MessageBox.Show("The inserted disc is not blank.", "Error");
                return false;
            }
            int result = ProgressDialog.ShowProgressDialog("Recording", _DoRecord, device, jolietImage);
            return result == 0;
        }

        private int _DoRecord(ProgressCallback callback, params object[] p)
        {
            StarBurn.CDevice device = p[0] as StarBurn.CDevice;
            StarBurn.CJolietImage jolietImage = p[1] as StarBurn.CJolietImage;
            CallBack cb = new CallBack(callback);
            try
            {
                device.Callback = cb;
                device.TestUnitReady();
                device.SetSpeeds(0xFFFF, 0xFFFF); //max speed

                bool BUPSupported = false;
                bool BUPEnabled = false;
                device.GetBUP(out BUPEnabled, out BUPSupported);
                device.SetBUP(true);
                device.SendOPC();
                device.TrackAtOnceFromFileSystemHandle((int)jolietImage.FileSystemHandle, false, true);
                device.Eject();
            }
            catch
            {
                MessageBox.Show("Exception = " + device.ErrorMessage + "\n" + jolietImage.ErrorMessage);
                return 1;
            }
            return 0;
        }

        private void _UpdateDevices()
        {
            cbDevices.Items.Clear();
            StarBurn.CDevices devices = new StarBurn.CDevicesClass();
            for (int i = 0; i < devices.Count; i++)
            {
                StarBurn.CDevice device = devices.GetDevice(i);
                cbDevices.Items.Add(/*Device.DeviceName +" "+*/device.ProductID + " " + device.Revision + " " + device.VendorID);
                if (i == 0)
                    cbDevices.SelectedItem = cbDevices.Items[i];
            }
        }

        private void btnRecord_Click(object sender, EventArgs e)
        {
            try
            {
                foreach (ListViewItem lvi in lvCD.Items)
                {
                    if (!lvi.Checked)
                        continue;
                    Node node = lvi.Tag as Node;
                    ProgressDialog.ShowProgressDialog("Fetching songs", Program.App.FetchSourceSongs, node);
                    while (!_RecordNode(node));
                    Program.App.CleanBuffer(node);
                    lvi.Checked = false;
                }
                DialogResult = DialogResult.OK;
                Close();
            }
            catch { }
        }
    }

    public class CallBack : StarBurn.IStarBurnCallBack
    {
        private ProgressCallback _progressCallback;

        public CallBack(ProgressCallback progressCallback)
        {
            _progressCallback = progressCallback;
        }

        public void ProgressCallBack(int Percent, int Time)
        {
            _progressCallback(Percent);
        }
    }

    class RecodingAbortedException : Exception
    {
    }
}