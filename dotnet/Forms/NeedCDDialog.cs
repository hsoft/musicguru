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
    public delegate string NeedCDCallback(string locationName);

    public partial class NeedCDDialog : Form
    {
        public static string AskForCD(string locationName)
        {
            using (NeedCDDialog dlg = new NeedCDDialog())
            {
                dlg.Owner = Application.OpenForms[0];
                dlg.lblCDName.Text = locationName;
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    string s = (string)dlg.lbDrives.SelectedItem;
                    return s.Substring(0, 2) + "\\";
                }
            }
            return null;
        }

        public NeedCDDialog()
        {
            InitializeComponent();
            FillDriveList();
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
            if ((lbDrives.Items.Count > 0) && (lbDrives.SelectedIndex < 0))
                lbDrives.SelectedIndex = 0;
        }

        private void tmr_Tick(object sender, EventArgs e)
        {
            FillDriveList();
        }

        private void lbDrives_SelectedIndexChanged(object sender, EventArgs e)
        {
            btnOk.Enabled = lbDrives.SelectedIndex >= 0;
        }
    }
}