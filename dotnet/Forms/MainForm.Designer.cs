namespace musicGuru
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.colName = new HS.Controls.Tree.TreeColumn();
            this.colLocation = new HS.Controls.Tree.TreeColumn();
            this.colCount = new HS.Controls.Tree.TreeColumn();
            this.colSize = new HS.Controls.Tree.TreeColumn();
            this.colTime = new HS.Controls.Tree.TreeColumn();
            this.mm = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.miAddLocation = new System.Windows.Forms.ToolStripMenuItem();
            this.miUpdateCollection = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem3 = new System.Windows.Forms.ToolStripSeparator();
            this.miQuit = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem2 = new System.Windows.Forms.ToolStripMenuItem();
            this.cmActions = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.miNewFolder = new System.Windows.Forms.ToolStripMenuItem();
            this.miRenameSelected = new System.Windows.Forms.ToolStripMenuItem();
            this.miSendToIgnoreBox = new System.Windows.Forms.ToolStripMenuItem();
            this.miSwitchConflict = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem5 = new System.Windows.Forms.ToolStripSeparator();
            this.miMassRename = new System.Windows.Forms.ToolStripMenuItem();
            this.miSplit = new System.Windows.Forms.ToolStripMenuItem();
            this.miRemoveEmptyFolders = new System.Windows.Forms.ToolStripMenuItem();
            this.miMoveConflicts = new System.Windows.Forms.ToolStripMenuItem();
            this.miMoveConflictsAndOriginal = new System.Windows.Forms.ToolStripMenuItem();
            this.tsbActions = new System.Windows.Forms.ToolStripDropDownButton();
            this.toolStripMenuItem4 = new System.Windows.Forms.ToolStripMenuItem();
            this.cmMaterialize = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.miMaterializeRename = new System.Windows.Forms.ToolStripMenuItem();
            this.miMaterializeCopy = new System.Windows.Forms.ToolStripMenuItem();
            this.miMaterializeMove = new System.Windows.Forms.ToolStripMenuItem();
            this.miMaterializeBurn = new System.Windows.Forms.ToolStripMenuItem();
            this.tsbMaterialize = new System.Windows.Forms.ToolStripDropDownButton();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.miLocations = new System.Windows.Forms.ToolStripMenuItem();
            this.miDetails = new System.Windows.Forms.ToolStripMenuItem();
            this.miIgnoreBox = new System.Windows.Forms.ToolStripMenuItem();
            this.helpToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.miHelp = new System.Windows.Forms.ToolStripMenuItem();
            this.miRegister = new System.Windows.Forms.ToolStripMenuItem();
            this.miCheckForUpdate = new System.Windows.Forms.ToolStripMenuItem();
            this.miAbout = new System.Windows.Forms.ToolStripMenuItem();
            this.ts = new System.Windows.Forms.ToolStrip();
            this.tsbLocations = new System.Windows.Forms.ToolStripButton();
            this.tsbDetails = new System.Windows.Forms.ToolStripButton();
            this.tsbIgnoreBox = new System.Windows.Forms.ToolStripButton();
            this.tvBoard = new HS.Controls.Tree.TreeViewAdv();
            this.ncIcon = new HS.Controls.Tree.NodeControls.NodeStateIcon();
            this.ncName = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncLocation = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncSongs = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncSize = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncTime = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.mm.SuspendLayout();
            this.cmActions.SuspendLayout();
            this.cmMaterialize.SuspendLayout();
            this.ts.SuspendLayout();
            this.SuspendLayout();
            // 
            // colName
            // 
            this.colName.Header = "Name";
            this.colName.Width = 250;
            // 
            // colLocation
            // 
            this.colLocation.Header = "Location";
            this.colLocation.Width = 100;
            // 
            // colCount
            // 
            this.colCount.Header = "Songs";
            // 
            // colSize
            // 
            this.colSize.Header = "Size (MB)";
            this.colSize.Width = 60;
            // 
            // colTime
            // 
            this.colTime.Header = "Time";
            this.colTime.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // mm
            // 
            this.mm.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.toolStripMenuItem2,
            this.toolStripMenuItem4,
            this.toolStripMenuItem1,
            this.helpToolStripMenuItem});
            this.mm.Location = new System.Drawing.Point(0, 0);
            this.mm.Name = "mm";
            this.mm.RenderMode = System.Windows.Forms.ToolStripRenderMode.System;
            this.mm.Size = new System.Drawing.Size(532, 24);
            this.mm.TabIndex = 0;
            this.mm.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.miAddLocation,
            this.miUpdateCollection,
            this.toolStripMenuItem3,
            this.miQuit});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // miAddLocation
            // 
            this.miAddLocation.Name = "miAddLocation";
            this.miAddLocation.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.A)));
            this.miAddLocation.Size = new System.Drawing.Size(211, 22);
            this.miAddLocation.Text = "Add Location";
            this.miAddLocation.Click += new System.EventHandler(this.miAddLocation_Click);
            // 
            // miUpdateCollection
            // 
            this.miUpdateCollection.Name = "miUpdateCollection";
            this.miUpdateCollection.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.U)));
            this.miUpdateCollection.Size = new System.Drawing.Size(211, 22);
            this.miUpdateCollection.Text = "Update Collection";
            this.miUpdateCollection.Click += new System.EventHandler(this.miUpdateCollection_Click);
            // 
            // toolStripMenuItem3
            // 
            this.toolStripMenuItem3.Name = "toolStripMenuItem3";
            this.toolStripMenuItem3.Size = new System.Drawing.Size(208, 6);
            // 
            // miQuit
            // 
            this.miQuit.Name = "miQuit";
            this.miQuit.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Q)));
            this.miQuit.Size = new System.Drawing.Size(211, 22);
            this.miQuit.Text = "Quit";
            this.miQuit.Click += new System.EventHandler(this.miQuit_Click);
            // 
            // toolStripMenuItem2
            // 
            this.toolStripMenuItem2.DropDown = this.cmActions;
            this.toolStripMenuItem2.Name = "toolStripMenuItem2";
            this.toolStripMenuItem2.Size = new System.Drawing.Size(59, 20);
            this.toolStripMenuItem2.Text = "Actions";
            // 
            // cmActions
            // 
            this.cmActions.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.miNewFolder,
            this.miRenameSelected,
            this.miSendToIgnoreBox,
            this.miSwitchConflict,
            this.toolStripMenuItem5,
            this.miMassRename,
            this.miSplit,
            this.miRemoveEmptyFolders,
            this.miMoveConflicts,
            this.miMoveConflictsAndOriginal});
            this.cmActions.Name = "cmActions";
            this.cmActions.OwnerItem = this.toolStripMenuItem2;
            this.cmActions.RenderMode = System.Windows.Forms.ToolStripRenderMode.System;
            this.cmActions.Size = new System.Drawing.Size(297, 208);
            // 
            // miNewFolder
            // 
            this.miNewFolder.Name = "miNewFolder";
            this.miNewFolder.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.N)));
            this.miNewFolder.Size = new System.Drawing.Size(296, 22);
            this.miNewFolder.Text = "New Folder";
            this.miNewFolder.Click += new System.EventHandler(this.miNewFolder_Click);
            // 
            // miRenameSelected
            // 
            this.miRenameSelected.Name = "miRenameSelected";
            this.miRenameSelected.ShortcutKeys = System.Windows.Forms.Keys.F2;
            this.miRenameSelected.Size = new System.Drawing.Size(296, 22);
            this.miRenameSelected.Text = "Rename Selected";
            this.miRenameSelected.Click += new System.EventHandler(this.miRenameSelected_Click);
            // 
            // miSendToIgnoreBox
            // 
            this.miSendToIgnoreBox.Name = "miSendToIgnoreBox";
            this.miSendToIgnoreBox.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.B)));
            this.miSendToIgnoreBox.Size = new System.Drawing.Size(296, 22);
            this.miSendToIgnoreBox.Text = "Send Selected to Ignore Box";
            this.miSendToIgnoreBox.Click += new System.EventHandler(this.miSendToIgnoreBox_Click);
            // 
            // miSwitchConflict
            // 
            this.miSwitchConflict.Name = "miSwitchConflict";
            this.miSwitchConflict.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.X)));
            this.miSwitchConflict.Size = new System.Drawing.Size(296, 22);
            this.miSwitchConflict.Text = "Switch Conflict and Original";
            this.miSwitchConflict.Click += new System.EventHandler(this.miSwitchConflict_Click);
            // 
            // toolStripMenuItem5
            // 
            this.toolStripMenuItem5.Name = "toolStripMenuItem5";
            this.toolStripMenuItem5.Size = new System.Drawing.Size(293, 6);
            // 
            // miMassRename
            // 
            this.miMassRename.Name = "miMassRename";
            this.miMassRename.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.R)));
            this.miMassRename.Size = new System.Drawing.Size(296, 22);
            this.miMassRename.Text = "Mass Rename";
            this.miMassRename.Click += new System.EventHandler(this.miMassRename_Click);
            // 
            // miSplit
            // 
            this.miSplit.Name = "miSplit";
            this.miSplit.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.miSplit.Size = new System.Drawing.Size(296, 22);
            this.miSplit.Text = "Split to CD/DVD";
            this.miSplit.Click += new System.EventHandler(this.miSplit_Click);
            // 
            // miRemoveEmptyFolders
            // 
            this.miRemoveEmptyFolders.Name = "miRemoveEmptyFolders";
            this.miRemoveEmptyFolders.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.E)));
            this.miRemoveEmptyFolders.Size = new System.Drawing.Size(296, 22);
            this.miRemoveEmptyFolders.Text = "Remove Empty Folders";
            this.miRemoveEmptyFolders.Click += new System.EventHandler(this.miRemoveEmptyFolders_Click);
            // 
            // miMoveConflicts
            // 
            this.miMoveConflicts.Name = "miMoveConflicts";
            this.miMoveConflicts.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.C)));
            this.miMoveConflicts.Size = new System.Drawing.Size(296, 22);
            this.miMoveConflicts.Text = "Move Conflicts";
            this.miMoveConflicts.Click += new System.EventHandler(this.miMoveConflicts_Click);
            // 
            // miMoveConflictsAndOriginal
            // 
            this.miMoveConflictsAndOriginal.Name = "miMoveConflictsAndOriginal";
            this.miMoveConflictsAndOriginal.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift)
                        | System.Windows.Forms.Keys.C)));
            this.miMoveConflictsAndOriginal.Size = new System.Drawing.Size(296, 22);
            this.miMoveConflictsAndOriginal.Text = "Move Conflicts and Original";
            this.miMoveConflictsAndOriginal.Click += new System.EventHandler(this.miMoveConflicts_Click);
            // 
            // tsbActions
            // 
            this.tsbActions.AutoSize = false;
            this.tsbActions.DropDown = this.cmActions;
            this.tsbActions.Image = global::musicGuru.Properties.Resources.actions_32;
            this.tsbActions.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.tsbActions.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbActions.Margin = new System.Windows.Forms.Padding(16, 1, 0, 2);
            this.tsbActions.Name = "tsbActions";
            this.tsbActions.Size = new System.Drawing.Size(75, 49);
            this.tsbActions.Text = "Actions";
            this.tsbActions.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            // 
            // toolStripMenuItem4
            // 
            this.toolStripMenuItem4.DropDown = this.cmMaterialize;
            this.toolStripMenuItem4.Name = "toolStripMenuItem4";
            this.toolStripMenuItem4.Size = new System.Drawing.Size(76, 20);
            this.toolStripMenuItem4.Text = "Materialize";
            // 
            // cmMaterialize
            // 
            this.cmMaterialize.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.miMaterializeRename,
            this.miMaterializeCopy,
            this.miMaterializeMove,
            this.miMaterializeBurn});
            this.cmMaterialize.Name = "cmMaterialize";
            this.cmMaterialize.OwnerItem = this.toolStripMenuItem4;
            this.cmMaterialize.RenderMode = System.Windows.Forms.ToolStripRenderMode.System;
            this.cmMaterialize.Size = new System.Drawing.Size(310, 92);
            // 
            // miMaterializeRename
            // 
            this.miMaterializeRename.Name = "miMaterializeRename";
            this.miMaterializeRename.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift)
                        | System.Windows.Forms.Keys.D1)));
            this.miMaterializeRename.Size = new System.Drawing.Size(309, 22);
            this.miMaterializeRename.Text = "Rename in respective locations";
            this.miMaterializeRename.Click += new System.EventHandler(this.miMaterializeRename_Click);
            // 
            // miMaterializeCopy
            // 
            this.miMaterializeCopy.Name = "miMaterializeCopy";
            this.miMaterializeCopy.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift)
                        | System.Windows.Forms.Keys.D2)));
            this.miMaterializeCopy.Size = new System.Drawing.Size(309, 22);
            this.miMaterializeCopy.Text = "Copy to other location";
            this.miMaterializeCopy.Click += new System.EventHandler(this.miMaterializeCopy_Click);
            // 
            // miMaterializeMove
            // 
            this.miMaterializeMove.Name = "miMaterializeMove";
            this.miMaterializeMove.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift)
                        | System.Windows.Forms.Keys.D3)));
            this.miMaterializeMove.Size = new System.Drawing.Size(309, 22);
            this.miMaterializeMove.Text = "Move to other location";
            this.miMaterializeMove.Click += new System.EventHandler(this.miMaterializeCopy_Click);
            // 
            // miMaterializeBurn
            // 
            this.miMaterializeBurn.Name = "miMaterializeBurn";
            this.miMaterializeBurn.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift)
                        | System.Windows.Forms.Keys.D4)));
            this.miMaterializeBurn.Size = new System.Drawing.Size(309, 22);
            this.miMaterializeBurn.Text = "Record to CDs/DVDs";
            this.miMaterializeBurn.Click += new System.EventHandler(this.miMaterializeBurn_Click);
            // 
            // tsbMaterialize
            // 
            this.tsbMaterialize.AutoSize = false;
            this.tsbMaterialize.DropDown = this.cmMaterialize;
            this.tsbMaterialize.Image = global::musicGuru.Properties.Resources.materialize_32;
            this.tsbMaterialize.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.tsbMaterialize.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbMaterialize.Name = "tsbMaterialize";
            this.tsbMaterialize.Size = new System.Drawing.Size(75, 49);
            this.tsbMaterialize.Text = "Materialize";
            this.tsbMaterialize.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.miLocations,
            this.miDetails,
            this.miIgnoreBox});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(63, 20);
            this.toolStripMenuItem1.Text = "Window";
            // 
            // miLocations
            // 
            this.miLocations.Name = "miLocations";
            this.miLocations.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.D1)));
            this.miLocations.Size = new System.Drawing.Size(170, 22);
            this.miLocations.Text = "Locations";
            this.miLocations.Click += new System.EventHandler(this.miLocations_Click);
            // 
            // miDetails
            // 
            this.miDetails.Name = "miDetails";
            this.miDetails.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.D2)));
            this.miDetails.Size = new System.Drawing.Size(170, 22);
            this.miDetails.Text = "Details";
            this.miDetails.Click += new System.EventHandler(this.miDetails_Click);
            // 
            // miIgnoreBox
            // 
            this.miIgnoreBox.Name = "miIgnoreBox";
            this.miIgnoreBox.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.D3)));
            this.miIgnoreBox.Size = new System.Drawing.Size(170, 22);
            this.miIgnoreBox.Text = "Ignore Box";
            this.miIgnoreBox.Click += new System.EventHandler(this.miIgnoreBox_Click);
            // 
            // helpToolStripMenuItem
            // 
            this.helpToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.miHelp,
            this.miRegister,
            this.miCheckForUpdate,
            this.miAbout});
            this.helpToolStripMenuItem.Name = "helpToolStripMenuItem";
            this.helpToolStripMenuItem.Size = new System.Drawing.Size(44, 20);
            this.helpToolStripMenuItem.Text = "Help";
            // 
            // miHelp
            // 
            this.miHelp.Name = "miHelp";
            this.miHelp.ShortcutKeys = System.Windows.Forms.Keys.F1;
            this.miHelp.Size = new System.Drawing.Size(179, 22);
            this.miHelp.Text = "musicGuru Help";
            this.miHelp.Click += new System.EventHandler(this.miHelp_Click);
            // 
            // miRegister
            // 
            this.miRegister.Name = "miRegister";
            this.miRegister.Size = new System.Drawing.Size(179, 22);
            this.miRegister.Text = "Register musicGuru";
            this.miRegister.Click += new System.EventHandler(this.miRegister_Click);
            // 
            // miCheckForUpdate
            // 
            this.miCheckForUpdate.Name = "miCheckForUpdate";
            this.miCheckForUpdate.Size = new System.Drawing.Size(179, 22);
            this.miCheckForUpdate.Text = "Check for update";
            this.miCheckForUpdate.Click += new System.EventHandler(this.miCheckForUpdate_Click);
            // 
            // miAbout
            // 
            this.miAbout.Name = "miAbout";
            this.miAbout.Size = new System.Drawing.Size(179, 22);
            this.miAbout.Text = "About musicGuru";
            this.miAbout.Click += new System.EventHandler(this.miAbout_Click);
            // 
            // ts
            // 
            this.ts.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden;
            this.ts.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tsbLocations,
            this.tsbDetails,
            this.tsbIgnoreBox,
            this.tsbActions,
            this.tsbMaterialize});
            this.ts.Location = new System.Drawing.Point(0, 24);
            this.ts.Name = "ts";
            this.ts.RenderMode = System.Windows.Forms.ToolStripRenderMode.System;
            this.ts.ShowItemToolTips = false;
            this.ts.Size = new System.Drawing.Size(532, 52);
            this.ts.TabIndex = 2;
            // 
            // tsbLocations
            // 
            this.tsbLocations.AutoSize = false;
            this.tsbLocations.Image = global::musicGuru.Properties.Resources.locations_32;
            this.tsbLocations.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.tsbLocations.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbLocations.Name = "tsbLocations";
            this.tsbLocations.Size = new System.Drawing.Size(75, 49);
            this.tsbLocations.Text = "Locations";
            this.tsbLocations.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.tsbLocations.Click += new System.EventHandler(this.miLocations_Click);
            // 
            // tsbDetails
            // 
            this.tsbDetails.AutoSize = false;
            this.tsbDetails.Image = global::musicGuru.Properties.Resources.details_32;
            this.tsbDetails.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.tsbDetails.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbDetails.Name = "tsbDetails";
            this.tsbDetails.Size = new System.Drawing.Size(75, 49);
            this.tsbDetails.Text = "Details";
            this.tsbDetails.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.tsbDetails.Click += new System.EventHandler(this.miDetails_Click);
            // 
            // tsbIgnoreBox
            // 
            this.tsbIgnoreBox.AutoSize = false;
            this.tsbIgnoreBox.Image = global::musicGuru.Properties.Resources.ignore_box_32;
            this.tsbIgnoreBox.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.tsbIgnoreBox.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbIgnoreBox.Name = "tsbIgnoreBox";
            this.tsbIgnoreBox.Size = new System.Drawing.Size(75, 49);
            this.tsbIgnoreBox.Text = "Ignore Box";
            this.tsbIgnoreBox.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.tsbIgnoreBox.Click += new System.EventHandler(this.miIgnoreBox_Click);
            // 
            // tvBoard
            // 
            this.tvBoard.AllowDrop = true;
            this.tvBoard.BackColor = System.Drawing.SystemColors.Window;
            this.tvBoard.Columns.Add(this.colName);
            this.tvBoard.Columns.Add(this.colLocation);
            this.tvBoard.Columns.Add(this.colCount);
            this.tvBoard.Columns.Add(this.colSize);
            this.tvBoard.Columns.Add(this.colTime);
            this.tvBoard.DefaultToolTipProvider = null;
            this.tvBoard.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tvBoard.DragDropMarkColor = System.Drawing.Color.Black;
            this.tvBoard.FullRowSelect = true;
            this.tvBoard.LineColor = System.Drawing.SystemColors.ControlDark;
            this.tvBoard.Location = new System.Drawing.Point(0, 76);
            this.tvBoard.Model = null;
            this.tvBoard.Name = "tvBoard";
            this.tvBoard.NodeControls.Add(this.ncIcon);
            this.tvBoard.NodeControls.Add(this.ncName);
            this.tvBoard.NodeControls.Add(this.ncLocation);
            this.tvBoard.NodeControls.Add(this.ncSongs);
            this.tvBoard.NodeControls.Add(this.ncSize);
            this.tvBoard.NodeControls.Add(this.ncTime);
            this.tvBoard.SelectedNode = null;
            this.tvBoard.Size = new System.Drawing.Size(532, 370);
            this.tvBoard.TabIndex = 3;
            this.tvBoard.ItemDrag += new System.Windows.Forms.ItemDragEventHandler(this.tvBoard_ItemDrag);
            this.tvBoard.DragOver += new System.Windows.Forms.DragEventHandler(this.tvBoard_DragOver);
            this.tvBoard.SelectionChanged += new System.EventHandler(this.tvBoard_SelectionChanged);
            this.tvBoard.DragDrop += new System.Windows.Forms.DragEventHandler(this.tvBoard_DragDrop);
            // 
            // ncIcon
            // 
            this.ncIcon.ParentColumn = this.colName;
            this.ncIcon.VirtualMode = true;
            // 
            // ncName
            // 
            this.ncName.DataPropertyName = "Name";
            this.ncName.EditEnabled = true;
            this.ncName.ParentColumn = this.colName;
            this.ncName.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // ncLocation
            // 
            this.ncLocation.DataPropertyName = "Location";
            this.ncLocation.ParentColumn = this.colLocation;
            this.ncLocation.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // ncSongs
            // 
            this.ncSongs.DataPropertyName = "Songs";
            this.ncSongs.ParentColumn = this.colCount;
            this.ncSongs.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // ncSize
            // 
            this.ncSize.DataPropertyName = "Size";
            this.ncSize.ParentColumn = this.colSize;
            this.ncSize.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // ncTime
            // 
            this.ncTime.DataPropertyName = "Time";
            this.ncTime.ParentColumn = this.colTime;
            this.ncTime.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.ncTime.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(532, 446);
            this.Controls.Add(this.tvBoard);
            this.Controls.Add(this.ts);
            this.Controls.Add(this.mm);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.mm;
            this.Name = "MainForm";
            this.Text = "musicGuru";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.mm.ResumeLayout(false);
            this.mm.PerformLayout();
            this.cmActions.ResumeLayout(false);
            this.cmMaterialize.ResumeLayout(false);
            this.ts.ResumeLayout(false);
            this.ts.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip mm;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem miQuit;
        private System.Windows.Forms.ToolStripMenuItem helpToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem miAbout;
        private System.Windows.Forms.ToolStripMenuItem miRegister;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncName;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncLocation;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncSongs;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncSize;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncTime;
        private System.Windows.Forms.ToolStrip ts;
        private System.Windows.Forms.ToolStripButton tsbDetails;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem miDetails;
        private HS.Controls.Tree.TreeViewAdv tvBoard;
        private System.Windows.Forms.ToolStripButton tsbLocations;
        private System.Windows.Forms.ToolStripButton tsbIgnoreBox;
        private System.Windows.Forms.ToolStripMenuItem miAddLocation;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem3;
        private System.Windows.Forms.ToolStripMenuItem miLocations;
        private System.Windows.Forms.ToolStripDropDownButton tsbActions;
        private System.Windows.Forms.ToolStripDropDownButton tsbMaterialize;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem2;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem4;
        private HS.Controls.Tree.NodeControls.NodeStateIcon ncIcon;
        private System.Windows.Forms.ContextMenuStrip cmActions;
        private System.Windows.Forms.ToolStripMenuItem miNewFolder;
        private System.Windows.Forms.ToolStripMenuItem miRenameSelected;
        private System.Windows.Forms.ToolStripMenuItem miSendToIgnoreBox;
        private System.Windows.Forms.ToolStripMenuItem miSwitchConflict;
        private System.Windows.Forms.ToolStripSeparator toolStripMenuItem5;
        private System.Windows.Forms.ToolStripMenuItem miMassRename;
        private System.Windows.Forms.ToolStripMenuItem miSplit;
        private System.Windows.Forms.ToolStripMenuItem miRemoveEmptyFolders;
        private System.Windows.Forms.ToolStripMenuItem miMoveConflicts;
        private System.Windows.Forms.ToolStripMenuItem miMoveConflictsAndOriginal;
        private System.Windows.Forms.ContextMenuStrip cmMaterialize;
        private System.Windows.Forms.ToolStripMenuItem miMaterializeRename;
        private System.Windows.Forms.ToolStripMenuItem miMaterializeCopy;
        private System.Windows.Forms.ToolStripMenuItem miMaterializeMove;
        private System.Windows.Forms.ToolStripMenuItem miMaterializeBurn;
        private System.Windows.Forms.ToolStripMenuItem miIgnoreBox;
        private System.Windows.Forms.ToolStripMenuItem miUpdateCollection;
        private System.Windows.Forms.ToolStripMenuItem miHelp;
        private System.Windows.Forms.ToolStripMenuItem miCheckForUpdate;
        private HS.Controls.Tree.TreeColumn colName;
        private HS.Controls.Tree.TreeColumn colLocation;
        private HS.Controls.Tree.TreeColumn colCount;
        private HS.Controls.Tree.TreeColumn colSize;
        private HS.Controls.Tree.TreeColumn colTime;
    }
}

