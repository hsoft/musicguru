using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using HS.Dialogs;

namespace musicGuru
{
    public partial class LocationForm : Form
    {
        public LocationForm()
        {
            InitializeComponent();
            RefreshLocations();
        }

        public Location SelectedLocation
        {
            get { return lvLocations.SelectedItems.Count > 0 ? (Location)lvLocations.SelectedItems[0].Tag : null; }
        }

        public void RefreshLocations()
        {
            lvLocations.ItemCheck -= this.lvLocations_ItemCheck; // We don't want to actually generate a location toggle when setting lvi.Checked
            int selectedIndex = lvLocations.SelectedIndices.Count > 0 ? lvLocations.SelectedIndices[0] : -1;
            lvLocations.Items.Clear();
            foreach (musicGuru.Location loc in Program.App.GetLocations())
            {
                ListViewItem lvi = lvLocations.Items.Add(loc.Name);
                lvi.SubItems.Add(loc.Songs);
                lvi.SubItems.Add(loc.Size);
                lvi.Tag = loc;
                lvi.ImageIndex = loc.IsRemovable ? 1 : 0;
                lvi.ForeColor = loc.IsAvailable ? Color.Black : Color.Red;
                lvi.Checked = Program.App.Board.ContainsLocation(loc);
            }
            if (selectedIndex >= 0)
                lvLocations.SelectedIndices.Add(selectedIndex);
            lvLocations.ItemCheck += this.lvLocations_ItemCheck;
        }

        private void btnRemove_Click(object sender, EventArgs e)
        {
            if (lvLocations.SelectedIndices.Count == 0)
                return;
            OnRequestRemoveLocation();
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            OnRequestAddLocation();
        }

        private void lvLocations_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            if (Program.App.Board.Splitted)
            {
                MessageBox.Show("You cannot add or remove location from the design board while it is splitted. Unsplit it first.");
                e.NewValue = e.CurrentValue;
                return;
            }
            OnLocationChecked(e);
        }

        private void lvLocations_SelectedIndexChanged(object sender, EventArgs e)
        {
            Location loc = this.SelectedLocation;
            if (loc != null)
            {
                lblPath.Text = loc.Path;
                lblType.Text = loc.IsRemovable ? "Removable (CD/DVD)" : "Fixed (Hard drive)";
                btnChangePath.Enabled = !loc.IsRemovable;
            }
            else
            {
                lblPath.Text = "";
                lblType.Text = "";
                btnChangePath.Enabled = false;
            }
        }

        public event EventHandler RequestAddLocation;
        private void OnRequestAddLocation()
        {
            if (RequestAddLocation != null)
                RequestAddLocation(this, EventArgs.Empty);
        }

        public event EventHandler RequestRemoveLocation;
        private void OnRequestRemoveLocation()
        {
            if (RequestRemoveLocation != null)
                RequestRemoveLocation(this, EventArgs.Empty);
        }

        public event EventHandler<LocationCheckEventArgs> LocationChecked;
        private void OnLocationChecked(ItemCheckEventArgs e)
        {
            if (LocationChecked != null)
            {
                LocationCheckEventArgs theEvent = new LocationCheckEventArgs((Location)lvLocations.Items[e.Index].Tag, e.NewValue == CheckState.Checked);
                LocationChecked(this, theEvent);
                if (!theEvent.CanCheck)
                    e.NewValue = e.CurrentValue;
            }
        }

        private void btnChangePath_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dlg = new FolderBrowserDialog())
            {
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    Location loc = this.SelectedLocation;
                    loc.Path = dlg.SelectedPath;
                    ProgressDialog.ShowProgressDialog("Updating Volume", Program.App.UpdateVolume, loc);
                    this.RefreshLocations();
                }
            }
        }
    }

    public class LocationCheckEventArgs : EventArgs
    {
        private Location _location;
        public Location Location
        {
            get { return _location; }
        }

        private bool _isChecked;
        public bool IsChecked
        {
            get { return _isChecked; }
        }

        private bool _canCheck;
        public bool CanCheck
        {
            get { return _canCheck; }
            set { _canCheck = value; }
        }

        public LocationCheckEventArgs(Location location, bool isChecked)
        {
            _location = location;
            _isChecked = isChecked;
            _canCheck = true;
        }
    }
}