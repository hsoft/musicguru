namespace musicGuru
{
    partial class LocationForm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(LocationForm));
            this.panel1 = new System.Windows.Forms.Panel();
            this.label3 = new System.Windows.Forms.Label();
            this.lblType = new System.Windows.Forms.Label();
            this.lblPath = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.btnRemove = new System.Windows.Forms.Button();
            this.btnAdd = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.lvLocations = new System.Windows.Forms.ListView();
            this.colName = new System.Windows.Forms.ColumnHeader();
            this.colSongs = new System.Windows.Forms.ColumnHeader();
            this.colSize = new System.Windows.Forms.ColumnHeader();
            this.il = new System.Windows.Forms.ImageList(this.components);
            this.btnChangePath = new System.Windows.Forms.Button();
            this.panel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.btnChangePath);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.lblType);
            this.panel1.Controls.Add(this.lblPath);
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.btnRemove);
            this.panel1.Controls.Add(this.btnAdd);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panel1.Location = new System.Drawing.Point(0, 164);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(284, 72);
            this.panel1.TabIndex = 1;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(34, 13);
            this.label3.TabIndex = 5;
            this.label3.Text = "Type:";
            // 
            // lblType
            // 
            this.lblType.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.lblType.Location = new System.Drawing.Point(50, 22);
            this.lblType.Name = "lblType";
            this.lblType.Size = new System.Drawing.Size(222, 13);
            this.lblType.TabIndex = 4;
            // 
            // lblPath
            // 
            this.lblPath.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.lblPath.Location = new System.Drawing.Point(50, 3);
            this.lblPath.Name = "lblPath";
            this.lblPath.Size = new System.Drawing.Size(222, 13);
            this.lblPath.TabIndex = 4;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 3);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(32, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Path:";
            // 
            // btnRemove
            // 
            this.btnRemove.Location = new System.Drawing.Point(116, 41);
            this.btnRemove.Name = "btnRemove";
            this.btnRemove.Size = new System.Drawing.Size(75, 23);
            this.btnRemove.TabIndex = 1;
            this.btnRemove.Text = "Remove";
            this.btnRemove.UseVisualStyleBackColor = true;
            this.btnRemove.Click += new System.EventHandler(this.btnRemove_Click);
            // 
            // btnAdd
            // 
            this.btnAdd.Location = new System.Drawing.Point(197, 41);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Size = new System.Drawing.Size(75, 23);
            this.btnAdd.TabIndex = 2;
            this.btnAdd.Text = "Add";
            this.btnAdd.UseVisualStyleBackColor = true;
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(3, 41);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(109, 28);
            this.label1.TabIndex = 2;
            this.label1.Text = "Check location to add to design board.";
            // 
            // lvLocations
            // 
            this.lvLocations.CheckBoxes = true;
            this.lvLocations.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.colName,
            this.colSongs,
            this.colSize});
            this.lvLocations.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lvLocations.FullRowSelect = true;
            this.lvLocations.HeaderStyle = System.Windows.Forms.ColumnHeaderStyle.Nonclickable;
            this.lvLocations.HideSelection = false;
            this.lvLocations.Location = new System.Drawing.Point(0, 0);
            this.lvLocations.MultiSelect = false;
            this.lvLocations.Name = "lvLocations";
            this.lvLocations.Size = new System.Drawing.Size(284, 164);
            this.lvLocations.SmallImageList = this.il;
            this.lvLocations.TabIndex = 0;
            this.lvLocations.UseCompatibleStateImageBehavior = false;
            this.lvLocations.View = System.Windows.Forms.View.Details;
            this.lvLocations.SelectedIndexChanged += new System.EventHandler(this.lvLocations_SelectedIndexChanged);
            this.lvLocations.ItemCheck += new System.Windows.Forms.ItemCheckEventHandler(this.lvLocations_ItemCheck);
            // 
            // colName
            // 
            this.colName.Text = "Location";
            this.colName.Width = 170;
            // 
            // colSongs
            // 
            this.colSongs.Text = "Songs";
            // 
            // colSize
            // 
            this.colSize.Text = "GB";
            this.colSize.Width = 50;
            // 
            // il
            // 
            this.il.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("il.ImageStream")));
            this.il.TransparentColor = System.Drawing.Color.White;
            this.il.Images.SetKeyName(0, "hdd.bmp");
            this.il.Images.SetKeyName(1, "cdrom.bmp");
            // 
            // btnChangePath
            // 
            this.btnChangePath.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btnChangePath.Location = new System.Drawing.Point(228, 3);
            this.btnChangePath.Name = "btnChangePath";
            this.btnChangePath.Size = new System.Drawing.Size(53, 21);
            this.btnChangePath.TabIndex = 0;
            this.btnChangePath.Text = "Change";
            this.btnChangePath.UseVisualStyleBackColor = true;
            this.btnChangePath.Click += new System.EventHandler(this.btnChangePath_Click);
            // 
            // LocationForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(284, 236);
            this.Controls.Add(this.lvLocations);
            this.Controls.Add(this.panel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.SizableToolWindow;
            this.Name = "LocationForm";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.Manual;
            this.Text = "Locations";
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button btnRemove;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.ListView lvLocations;
        private System.Windows.Forms.ColumnHeader colName;
        private System.Windows.Forms.ColumnHeader colSongs;
        private System.Windows.Forms.ColumnHeader colSize;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ImageList il;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lblType;
        private System.Windows.Forms.Label lblPath;
        private System.Windows.Forms.Button btnChangePath;
    }
}