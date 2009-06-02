namespace musicGuru
{
    partial class IgnoreBox
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
            this.colName = new HS.Controls.Tree.TreeColumn();
            this.colLocation = new HS.Controls.Tree.TreeColumn();
            this.colCount = new HS.Controls.Tree.TreeColumn();
            this.colSize = new HS.Controls.Tree.TreeColumn();
            this.colTime = new HS.Controls.Tree.TreeColumn();
            this.label1 = new System.Windows.Forms.Label();
            this.tvIgnoreBox = new HS.Controls.Tree.TreeViewAdv();
            this.ncIcon = new HS.Controls.Tree.NodeControls.NodeStateIcon();
            this.ncName = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncLocation = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncSongs = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncSize = new HS.Controls.Tree.NodeControls.NodeTextBox();
            this.ncTime = new HS.Controls.Tree.NodeControls.NodeTextBox();
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
            // label1
            // 
            this.label1.Dock = System.Windows.Forms.DockStyle.Top;
            this.label1.Location = new System.Drawing.Point(0, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(532, 18);
            this.label1.TabIndex = 0;
            this.label1.Text = "Items dragged to the ignore box will not be materialized";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tvIgnoreBox
            // 
            this.tvIgnoreBox.AllowDrop = true;
            this.tvIgnoreBox.BackColor = System.Drawing.SystemColors.Window;
            this.tvIgnoreBox.Columns.Add(this.colName);
            this.tvIgnoreBox.Columns.Add(this.colLocation);
            this.tvIgnoreBox.Columns.Add(this.colCount);
            this.tvIgnoreBox.Columns.Add(this.colSize);
            this.tvIgnoreBox.Columns.Add(this.colTime);
            this.tvIgnoreBox.DefaultToolTipProvider = null;
            this.tvIgnoreBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tvIgnoreBox.DragDropMarkColor = System.Drawing.Color.Black;
            this.tvIgnoreBox.FullRowSelect = true;
            this.tvIgnoreBox.LineColor = System.Drawing.SystemColors.ControlDark;
            this.tvIgnoreBox.Location = new System.Drawing.Point(0, 18);
            this.tvIgnoreBox.Model = null;
            this.tvIgnoreBox.Name = "tvIgnoreBox";
            this.tvIgnoreBox.NodeControls.Add(this.ncIcon);
            this.tvIgnoreBox.NodeControls.Add(this.ncName);
            this.tvIgnoreBox.NodeControls.Add(this.ncLocation);
            this.tvIgnoreBox.NodeControls.Add(this.ncSongs);
            this.tvIgnoreBox.NodeControls.Add(this.ncSize);
            this.tvIgnoreBox.NodeControls.Add(this.ncTime);
            this.tvIgnoreBox.SelectedNode = null;
            this.tvIgnoreBox.Size = new System.Drawing.Size(532, 172);
            this.tvIgnoreBox.TabIndex = 4;
            this.tvIgnoreBox.ItemDrag += new System.Windows.Forms.ItemDragEventHandler(this.tvIgnoreBox_ItemDrag);
            this.tvIgnoreBox.DragOver += new System.Windows.Forms.DragEventHandler(this.tvIgnoreBox_DragOver);
            this.tvIgnoreBox.DragDrop += new System.Windows.Forms.DragEventHandler(this.tvIgnoreBox_DragDrop);
            // 
            // ncIcon
            // 
            this.ncIcon.ParentColumn = this.colName;
            this.ncIcon.VirtualMode = true;
            // 
            // ncName
            // 
            this.ncName.DataPropertyName = "Name";
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
            this.ncTime.TextColor = System.Drawing.SystemColors.ControlText;
            // 
            // IgnoreBox
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(532, 190);
            this.Controls.Add(this.tvIgnoreBox);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.SizableToolWindow;
            this.Name = "IgnoreBox";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.Manual;
            this.Text = "Ignore Box";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private HS.Controls.Tree.TreeViewAdv tvIgnoreBox;
        private HS.Controls.Tree.NodeControls.NodeStateIcon ncIcon;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncName;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncLocation;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncSongs;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncSize;
        private HS.Controls.Tree.NodeControls.NodeTextBox ncTime;
        private HS.Controls.Tree.TreeColumn colName;
        private HS.Controls.Tree.TreeColumn colLocation;
        private HS.Controls.Tree.TreeColumn colCount;
        private HS.Controls.Tree.TreeColumn colSize;
        private HS.Controls.Tree.TreeColumn colTime;
    }
}