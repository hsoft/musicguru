namespace musicGuru
{
    partial class AddLocationDialog
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
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.rbRemovable = new System.Windows.Forms.RadioButton();
            this.rbFixed = new System.Windows.Forms.RadioButton();
            this.gbFixed = new System.Windows.Forms.GroupBox();
            this.btnBrowse = new System.Windows.Forms.Button();
            this.txtPath = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.gbRemovable = new System.Windows.Forms.GroupBox();
            this.lbDrives = new System.Windows.Forms.ListBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.txtLocationName = new System.Windows.Forms.TextBox();
            this.btnCancel = new System.Windows.Forms.Button();
            this.btnAdd = new System.Windows.Forms.Button();
            this.tmr = new System.Windows.Forms.Timer(this.components);
            this.groupBox1.SuspendLayout();
            this.gbFixed.SuspendLayout();
            this.gbRemovable.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.rbRemovable);
            this.groupBox1.Controls.Add(this.rbFixed);
            this.groupBox1.Location = new System.Drawing.Point(13, 13);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(304, 69);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Add songs from...";
            // 
            // rbRemovable
            // 
            this.rbRemovable.AutoSize = true;
            this.rbRemovable.Location = new System.Drawing.Point(7, 43);
            this.rbRemovable.Name = "rbRemovable";
            this.rbRemovable.Size = new System.Drawing.Size(224, 17);
            this.rbRemovable.TabIndex = 1;
            this.rbRemovable.Text = "A removable media (CD, DVD, USB Drive)";
            this.rbRemovable.UseVisualStyleBackColor = true;
            // 
            // rbFixed
            // 
            this.rbFixed.AutoSize = true;
            this.rbFixed.Checked = true;
            this.rbFixed.Location = new System.Drawing.Point(7, 19);
            this.rbFixed.Name = "rbFixed";
            this.rbFixed.Size = new System.Drawing.Size(183, 17);
            this.rbFixed.TabIndex = 0;
            this.rbFixed.TabStop = true;
            this.rbFixed.Text = "A fixed, writable drive (Hard drive)";
            this.rbFixed.UseVisualStyleBackColor = true;
            this.rbFixed.CheckedChanged += new System.EventHandler(this.rbFixed_CheckedChanged);
            // 
            // gbFixed
            // 
            this.gbFixed.Controls.Add(this.btnBrowse);
            this.gbFixed.Controls.Add(this.txtPath);
            this.gbFixed.Controls.Add(this.label1);
            this.gbFixed.Location = new System.Drawing.Point(12, 89);
            this.gbFixed.Name = "gbFixed";
            this.gbFixed.Size = new System.Drawing.Size(304, 100);
            this.gbFixed.TabIndex = 1;
            this.gbFixed.TabStop = false;
            this.gbFixed.Text = "Fixed drive";
            // 
            // btnBrowse
            // 
            this.btnBrowse.Location = new System.Drawing.Point(223, 63);
            this.btnBrowse.Name = "btnBrowse";
            this.btnBrowse.Size = new System.Drawing.Size(75, 23);
            this.btnBrowse.TabIndex = 2;
            this.btnBrowse.Text = "Browse";
            this.btnBrowse.UseVisualStyleBackColor = true;
            this.btnBrowse.Click += new System.EventHandler(this.btnBrowse_Click);
            // 
            // txtPath
            // 
            this.txtPath.Location = new System.Drawing.Point(11, 37);
            this.txtPath.Name = "txtPath";
            this.txtPath.Size = new System.Drawing.Size(287, 20);
            this.txtPath.TabIndex = 1;
            this.txtPath.TextChanged += new System.EventHandler(this.txtPath_TextChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(8, 20);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(155, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Where are your songs located?";
            // 
            // gbRemovable
            // 
            this.gbRemovable.Controls.Add(this.lbDrives);
            this.gbRemovable.Controls.Add(this.label2);
            this.gbRemovable.Location = new System.Drawing.Point(12, 89);
            this.gbRemovable.Name = "gbRemovable";
            this.gbRemovable.Size = new System.Drawing.Size(304, 100);
            this.gbRemovable.TabIndex = 2;
            this.gbRemovable.TabStop = false;
            this.gbRemovable.Text = "Removable media";
            this.gbRemovable.Visible = false;
            // 
            // lbDrives
            // 
            this.lbDrives.FormattingEnabled = true;
            this.lbDrives.Location = new System.Drawing.Point(13, 37);
            this.lbDrives.Name = "lbDrives";
            this.lbDrives.Size = new System.Drawing.Size(284, 56);
            this.lbDrives.TabIndex = 1;
            this.lbDrives.SelectedIndexChanged += new System.EventHandler(this.lbDrives_SelectedIndexChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(10, 20);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(241, 13);
            this.label2.TabIndex = 0;
            this.label2.Text = "Which drive do you want to add your songs from?";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(13, 196);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(79, 13);
            this.label3.TabIndex = 3;
            this.label3.Text = "Location Name";
            // 
            // txtLocationName
            // 
            this.txtLocationName.Location = new System.Drawing.Point(16, 213);
            this.txtLocationName.Name = "txtLocationName";
            this.txtLocationName.Size = new System.Drawing.Size(300, 20);
            this.txtLocationName.TabIndex = 4;
            // 
            // btnCancel
            // 
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(237, 239);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(80, 23);
            this.btnCancel.TabIndex = 5;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            // 
            // btnAdd
            // 
            this.btnAdd.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnAdd.Location = new System.Drawing.Point(151, 239);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Size = new System.Drawing.Size(80, 23);
            this.btnAdd.TabIndex = 6;
            this.btnAdd.Text = "Add Location";
            this.btnAdd.UseVisualStyleBackColor = true;
            // 
            // tmr
            // 
            this.tmr.Interval = 3000;
            this.tmr.Tick += new System.EventHandler(this.tmr_Tick);
            // 
            // AddLocationDialog
            // 
            this.AcceptButton = this.btnAdd;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btnCancel;
            this.ClientSize = new System.Drawing.Size(328, 270);
            this.Controls.Add(this.gbFixed);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.txtLocationName);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.gbRemovable);
            this.Controls.Add(this.groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "AddLocationDialog";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.Text = "Add Location";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.gbFixed.ResumeLayout(false);
            this.gbFixed.PerformLayout();
            this.gbRemovable.ResumeLayout(false);
            this.gbRemovable.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.RadioButton rbRemovable;
        private System.Windows.Forms.RadioButton rbFixed;
        private System.Windows.Forms.GroupBox gbFixed;
        private System.Windows.Forms.Button btnBrowse;
        private System.Windows.Forms.TextBox txtPath;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.GroupBox gbRemovable;
        private System.Windows.Forms.ListBox lbDrives;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txtLocationName;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Timer tmr;
    }
}