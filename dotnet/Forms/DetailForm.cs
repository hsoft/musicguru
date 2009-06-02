using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace musicGuru
{
    public partial class DetailForm : Form
    {
        public DetailForm()
        {
            InitializeComponent();
        }

        public void UpdateInfo(List<List<string>> info)
        {
            lvInfo.BeginUpdate();
            lvInfo.Items.Clear();
            foreach (List<string> pair in info)
            {
                ListViewItem lvi = lvInfo.Items.Add(pair[0]);
                lvi.SubItems.Add(pair[1]);
            }
            lvInfo.EndUpdate();
        }
    }
}