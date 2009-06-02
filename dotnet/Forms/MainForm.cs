using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using HS.Controls.Tree;
using HS.Controls.Tree.Base;
using HS.Controls.Tree.NodeControls;
using HS.Dialogs;

namespace musicGuru
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
            _UpdateRegistrationControls();
            tvBoard.Model = new NodeModel(Program.App.Board);
            ncIcon.ValueNeeded += ncIcon_ValueNeeded;
        }

        #region Properties

        private DetailForm _details = null;
        private LocationForm _locations = null;
        private IgnoreBox _ignoreBox = null;

        private DetailForm Details
        {
            get
            {
                if (_details == null)
                {
                    _details = new DetailForm();
                    _details.Disposed += Form_Disposed;
                    _details.Top = Bottom - _details.Height;
                    _details.Left = Right;
                    if (_details.Right > Screen.PrimaryScreen.WorkingArea.Right)
                        _details.Left = Screen.PrimaryScreen.WorkingArea.Right - _details.Width;
                    _details.Owner = this;
                }
                return _details;
            }
        }

        private LocationForm Locations
        {
            get
            {
                if (_locations == null)
                {
                    _locations = new LocationForm();
                    _locations.Disposed += Form_Disposed;
                    _locations.RequestAddLocation += Locations_RequestAddLocation;
                    _locations.RequestRemoveLocation += Locations_RequestRemoveLocation;
                    _locations.LocationChecked += Locations_LocationChecked;
                    _locations.Top = Top;
                    _locations.Left = Right;
                    if (_locations.Right > Screen.PrimaryScreen.WorkingArea.Right)
                    {
                        _locations.Left = Screen.PrimaryScreen.WorkingArea.Right - _locations.Width;
                        _locations.Top = Top + 32;
                    }
                    _locations.Owner = this;
                }
                return _locations;
            }
        }

        private IgnoreBox IgnoreBox
        {
            get
            {
                if (_ignoreBox == null)
                {
                    _ignoreBox = new IgnoreBox();
                    _ignoreBox.Disposed += Form_Disposed;
                    _ignoreBox.Top = Bottom;
                    _ignoreBox.Left = Left;
                    if (_ignoreBox.Bottom > Screen.PrimaryScreen.WorkingArea.Bottom)
                        _ignoreBox.Top = Screen.PrimaryScreen.WorkingArea.Bottom - _ignoreBox.Height;
                    _ignoreBox.Owner = this;
                }
                return _ignoreBox;
            }
        }

        #endregion

        #region Private

        private bool _DemoCheck()
        {
            if (!Preferences.Registered)
            {
                MessageBox.Show("You must register musicGuru to materialize your design board.");
                return false;
            }
            return true;
        }

        private List<Node> _GetSelection()
        {
            List<Node> selected = new List<Node>();
            foreach (TreeNodeAdv node in tvBoard.SelectedNodes)
                selected.Add((Node)node.Tag);
            return selected;
        }

        // Verify that all to-be-materialized locations are available.s
        private bool _LocationCheck()
        {
            Locations.RefreshLocations();
            foreach (Location loc in Program.App.GetLocations())
            {
                if ((Program.App.Board.ContainsLocation(loc)) && (!loc.IsAvailable))
                {
                    string format = "The location '{0}' at path '{1}' is unreachable. You can't materialize your design.";
                    string message = string.Format(format, loc.Name, loc.Path);
                    MessageBox.Show(message);
                    return false;
                }
            }
            return true;
        }

        private void _UpdateRegistrationControls()
        {
            if (Preferences.Registered)
            {
                Text = Application.ProductName;
                miRegister.Visible = false;
            }
            else
            {
                Text = Application.ProductName + " - DEMO";
                miRegister.Visible = true;
            }
        }

        #endregion

        #region Menu Clicks

        private void miAbout_Click(object sender, EventArgs e)
        {
            using (AboutBox box = new AboutBox())
            {
                box.ShowDialog();
            }
            _UpdateRegistrationControls();
        }

        private void miRegister_Click(object sender, EventArgs e)
        {
            Preferences.AskForCode();
            _UpdateRegistrationControls();
        }

        private void miQuit_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void miHelp_Click(object sender, EventArgs e)
        {
            Process.Start("help\\intro.htm");
        }

        private void miCheckForUpdate_Click(object sender, EventArgs e)
        {
            Process.Start("updater.exe", "/checknow");
        }

        private void miLocations_Click(object sender, EventArgs e)
        {
            Locations.Visible = !Locations.Visible;
            Focus();
        }

        private void miDetails_Click(object sender, EventArgs e)
        {
            Details.Visible = !Details.Visible;
            Focus();
        }

        private void miIgnoreBox_Click(object sender, EventArgs e)
        {
            IgnoreBox.Visible = !IgnoreBox.Visible;
            Focus();
        }

        private void miAddLocation_Click(object sender, EventArgs e)
        {
            using (AddLocationDialog dlg = new AddLocationDialog())
            {
                dlg.Owner = this;
                while (true)
                {
                    DialogResult r = dlg.ShowDialog();
                    if (r == DialogResult.Cancel)
                        break;
                    string canAdd = Program.App.CanAddLocation(dlg.LocPath, dlg.LocName);
                    if (canAdd.Length == 0)
                    {
                        ProgressDialog.ShowProgressDialog("Adding Location", Program.App.AddLocation,
                            dlg.LocPath, dlg.LocName, dlg.LocRemoveable);
                        if (_locations != null)
                            _locations.RefreshLocations();
                        break;
                    }
                    else
                        MessageBox.Show(canAdd);
                }
            }
        }

        private void miNewFolder_Click(object sender, EventArgs e)
        {
            Node node;
            TreeNodeAdv selected = tvBoard.SelectedNode;
            if (selected == null)
            {
                node = Program.App.Board;
                selected = tvBoard.Root;
            }
            else
            {
                node = selected.Tag as Node;
                if (!node.IsContainer)
                {
                    node = node.Parent;
                    selected = selected.Parent;
                }
            }
            Node newFolder = node.NewFolder();
            selected.IsExpanded = true;
            TreeNodeAdv newFolderNode = selected.FindNode(new TreePath(newFolder));
            tvBoard.SelectedNode = newFolderNode;
            ncName.BeginEdit();
        }

        private void miRenameSelected_Click(object sender, EventArgs e)
        {
            ncName.BeginEdit();
        }

        private void miRemoveEmptyFolders_Click(object sender, EventArgs e)
        {
            Program.App.RemoveEmptyDirs();
        }

        private void miMassRename_Click(object sender, EventArgs e)
        {
            if (Program.App.Board.Nodes.Count == 0)
                return;
            using (MassRenameDialog dlg = new MassRenameDialog())
            {
                dlg.Owner = this;
                if (dlg.ShowDialog() == DialogResult.OK)
                    ProgressDialog.ShowProgressDialog("Renaming", Program.App.MassRename,
                            dlg.panel.Model, dlg.panel.Whitespace);
            }
        }

        private void miSplit_Click(object sender, EventArgs e)
        {
            if (Program.App.Board.Nodes.Count == 0)
                return;
            if (Program.App.Board.Splitted)
            {
                Program.App.Unsplit();
            }
            else
            {
                using (SplitDialog dlg = new SplitDialog())
                {
                    dlg.Owner = this;
                    if (dlg.ShowDialog() == DialogResult.OK)
                        ProgressDialog.ShowProgressDialog("Splitting", Program.App.Split,
                                dlg.panel.Model, dlg.panel.Capacity, dlg.panel.GroupingLevel, dlg.panel.TruncateNameTo);
                }
            }
            if (Program.App.Board.Splitted)
                miSplit.Text = "Unsplit CD/DVD";
            else
                miSplit.Text = "Split to CD/DVD";
        }

        private void miSendToIgnoreBox_Click(object sender, EventArgs e)
        {
            foreach (Node node in _GetSelection())
                node.Move(Program.App.Board.IgnoreBox);
        }

        private void miSwitchConflict_Click(object sender, EventArgs e)
        {
            if (tvBoard.SelectedNode == null)
                return;
            Program.App.SwitchConflictAndOriginal(tvBoard.SelectedNode.Tag as Node);
        }

        private void miMoveConflicts_Click(object sender, EventArgs e)
        {
            Program.App.Board.MoveConflicts(sender == miMoveConflictsAndOriginal);
        }

        private void miUpdateCollection_Click(object sender, EventArgs e)
        {
            ProgressDialog.ShowProgressDialog("Updating Collection", Program.App.UpdateCollection);
        }

        private void miMaterializeRename_Click(object sender, EventArgs e)
        {
            if ((!_DemoCheck()) || (!_LocationCheck()) || (Program.App.Board.Nodes.Count == 0))
                return;
            if (MessageBox.Show("Songs in the board are going to be renamed in their respective locations.", "Confirmation", MessageBoxButtons.OKCancel, MessageBoxIcon.Question) == DialogResult.Cancel)
                return;
            int result = ProgressDialog.ShowProgressDialog("Renaming", Program.App.RenameInRespectiveLocations);
            if (result == 1)
                MessageBox.Show("You cannot perform a rename operation with read-only locations on the design board.");
            else
                Locations.RefreshLocations();
        }

        private void miMaterializeCopy_Click(object sender, EventArgs e)
        {
            if ((!_DemoCheck()) || (!_LocationCheck()) || (Program.App.Board.Nodes.Count == 0))
                return;
            bool copy = sender == miMaterializeCopy;
            using (FolderBrowserDialog dlg = new FolderBrowserDialog())
            {
                dlg.ShowNewFolderButton = true;
                dlg.Description = "Where do you want to copy songs in the design board to?";
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    ProgressDialog.ShowProgressDialog(copy ? "Copying" : "Moving", Program.App.CopyOrMove, copy, dlg.SelectedPath);
                    if (!copy)
                        Locations.RefreshLocations();
                }
            }
        }

        private void miMaterializeBurn_Click(object sender, EventArgs e)
        {
            if ((!_DemoCheck()) || (!_LocationCheck()) || (Program.App.Board.Nodes.Count == 0))
                return;
            if (!Program.App.Board.Splitted)
            {
                MessageBox.Show("You must split the design board before recording it to CD/DVD.");
                return;
            }
            using (RecordForm dlg = new RecordForm())
            {
                dlg.Owner = this;
                dlg.ShowDialog();
            }
        }

        #endregion

        #region Event handlers

        private void MainForm_Load(object sender, EventArgs e)
        {
            Locations.Show();
            Details.Show();
        }

        private void Form_Disposed(object sender, EventArgs e)
        {
            if (sender == _details)
                _details = null;
            if (sender == _locations)
                _locations = null;
            if (sender == _ignoreBox)
                _ignoreBox = null;
        }

        private void Locations_RequestAddLocation(object sender, EventArgs e)
        {
            miAddLocation_Click(this, e);
        }

        private void Locations_RequestRemoveLocation(object sender, EventArgs e)
        {
            Locations.SelectedLocation.RemoveFromCollection();
            Locations.RefreshLocations();
        }

        private void Locations_LocationChecked(object sender, LocationCheckEventArgs e)
        {
            e.Location.Toggle();
        }

        private void tvBoard_SelectionChanged(object sender, EventArgs e)
        {
            Details.UpdateInfo(Program.App.GetSelectionInfo(_GetSelection()));
        }

        private void tvBoard_ItemDrag(object sender, ItemDragEventArgs e)
        {
            tvBoard.DoDragDropSelectedNodes(DragDropEffects.Move);
        }

        private void tvBoard_DragOver(object sender, DragEventArgs e)
        {
            TreeNodeAdv[] nodes = e.Data.GetData(typeof(TreeNodeAdv[])) as TreeNodeAdv[];
            if (nodes.Length > 0)
                e.Effect = e.AllowedEffect;
        }

        private void tvBoard_DragDrop(object sender, DragEventArgs e)
        {
            TreeNodeAdv[] nodes = (TreeNodeAdv[])e.Data.GetData(typeof(TreeNodeAdv[]));
            Node dropNode;
            if (tvBoard.DropPosition.Node == null)
                dropNode = Program.App.Board;
            else
            {
                dropNode = tvBoard.DropPosition.Node.Tag as Node;
                if ((tvBoard.DropPosition.Position != NodePosition.Inside) || (!dropNode.IsContainer))
                    dropNode = dropNode.Parent;
            }
            tvBoard.BeginUpdate();
            foreach (TreeNodeAdv node in nodes)
                (node.Tag as Node).Move(dropNode);
            tvBoard.EndUpdate();
        }

        private void ncIcon_ValueNeeded(object sender, NodeControlValueEventArgs e)
        {
            Node node = (Node)e.Node.Tag;
            Bitmap bmp = (Bitmap)Properties.Resources.ResourceManager.GetObject(node.ImageName);
            bmp.MakeTransparent(Color.Fuchsia);
            e.Value = bmp;
        }

        #endregion
    }
}