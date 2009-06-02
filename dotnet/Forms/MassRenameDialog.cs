using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace musicGuru
{
    public partial class MassRenameDialog : Form
    {
        public MassRenamePanel panel;

        public MassRenameDialog()
        {
            InitializeComponent();
            panel = Program.App.GetMassRenamePanel();
            txtCustomModel.Text = Preferences.CustomModel;
            DisplayExampleSong();
        }

        private void DisplayExampleSong()
        {
            lblBefore.Text = panel.ExampleBefore;
            lblAfter.Text = panel.ExampleAfter;
        }

        private void rbModel_CheckedChanged(object sender, EventArgs e)
        {
            RadioButton rb = sender as RadioButton;
            if (rb.Checked)
            {
                panel.ModelIndex = Convert.ToInt32(rb.Tag);
                DisplayExampleSong();
                txtCustomModel.Enabled = Convert.ToInt32(rb.Tag) == 4;
            }
        }

        private void txtCustomModel_TextChanged(object sender, EventArgs e)
        {
            panel.CustomModel = txtCustomModel.Text;
            Preferences.CustomModel = txtCustomModel.Text;
            DisplayExampleSong();
        }

        private void btnChangeExample_Click(object sender, EventArgs e)
        {
            panel.ChangeExample();
            DisplayExampleSong();
        }

        private void rbWS_CheckedChanged(object sender, EventArgs e)
        {
            RadioButton rb = sender as RadioButton;
            if (rb.Checked)
            {
                panel.WhitespaceIndex = Convert.ToInt32(rb.Tag);
                DisplayExampleSong();
            }
        }
    }
}