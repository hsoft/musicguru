using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Management;
using System.IO;

namespace musicGuru
{
    public partial class AddLocationDialog : Form
    {
        public AddLocationDialog()
        {
            InitializeComponent();
        }

        private string _locPath = "";
        public string LocPath { get { return _locPath; } }
        public string LocName { get { return txtLocationName.Text; } }
        public bool LocRemoveable { get { return rbRemovable.Checked; } }

        private void rbFixed_CheckedChanged(object sender, EventArgs e)
        {
            gbFixed.Visible = rbFixed.Checked;
            gbRemovable.Visible = rbRemovable.Checked;
            if (rbRemovable.Checked)
                FillDriveList();
            tmr.Enabled = rbRemovable.Checked;
        }

        private void FillDriveList()
        {
            SelectQuery query = new SelectQuery("select * from win32_logicaldisk where drivetype=5");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(query);

            int i = 0;
            foreach (ManagementObject mo in searcher.Get())
            {
                string s = string.Format("{0} [{1}]", mo["deviceid"], mo["volumename"]);
                if (i >= lbDrives.Items.Count)
                    lbDrives.Items.Add(s);
                else
                    lbDrives.Items[i] = s;
            }
        }

        private void tmr_Tick(object sender, EventArgs e)
        {
            FillDriveList();
        }

        private void btnBrowse_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dlg = new FolderBrowserDialog())
            {
                if (dlg.ShowDialog() == DialogResult.OK)
                    txtPath.Text = dlg.SelectedPath;
            }
        }

        private void txtPath_TextChanged(object sender, EventArgs e)
        {
            txtLocationName.Text = Path.GetFileName(txtPath.Text);
            _locPath = txtPath.Text;
        }

        private void lbDrives_SelectedIndexChanged(object sender, EventArgs e)
        {
            string s = (string)lbDrives.SelectedItem;
            txtLocationName.Text = s.Substring(4, s.Length - 5);
            _locPath = s.Substring(0, 2) + "\\";
        }
    }
}