using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace musicGuru
{
    public partial class SplitDialog : Form
    {
        public SplitPanel panel;

        public SplitDialog()
        {
            InitializeComponent();
            panel = Program.App.GetSplitPanel();
            numCapacity_ValueChanged(this, EventArgs.Empty);
        }

        private void rbModel_CheckedChanged(object sender, EventArgs e)
        {
            RadioButton rb = sender as RadioButton;
            if (rb.Checked)
            {
                panel.ModelIndex = Convert.ToInt32(rb.Tag);
                txtCustomModel.Enabled = Convert.ToInt32(rb.Tag) == 3;
            }
        }

        private void rbCapacity_CheckedChanged(object sender, EventArgs e)
        {
            RadioButton rb = sender as RadioButton;
            if (rb.Checked)
            {
                panel.CapacityIndex = Convert.ToInt32(rb.Tag);
                numCapacity.Enabled = Convert.ToInt32(rb.Tag) == 3;
            }
        }

        private void tbGroupLevel_Scroll(object sender, EventArgs e)
        {
            panel.GroupingLevel = tbGroupLevel.Value;
            lblExample.Text = panel.Example;
        }

        private void btnChangeExample_Click(object sender, EventArgs e)
        {
            lblExample.Text = panel.Example;
        }

        private void cbTruncate_CheckedChanged(object sender, EventArgs e)
        {
            if (cbTruncate.Checked)
                panel.TruncateNameTo = 16;
            else
                panel.TruncateNameTo = 0;
        }

        private void numCapacity_ValueChanged(object sender, EventArgs e)
        {
            panel.CustomCapacity = Convert.ToInt64(numCapacity.Value) * 1024 * 1024;
        }
    }
}