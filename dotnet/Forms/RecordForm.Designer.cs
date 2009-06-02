namespace musicGuru
{
    partial class RecordForm
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
            this.label1 = new System.Windows.Forms.Label();
            this.lvCD = new System.Windows.Forms.ListView();
            this.colName = new System.Windows.Forms.ColumnHeader();
            this.colSongs = new System.Windows.Forms.ColumnHeader();
            this.colSize = new System.Windows.Forms.ColumnHeader();
            this.label2 = new System.Windows.Forms.Label();
            this.lblRequiredSpace = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.cbDevices = new System.Windows.Forms.ComboBox();
            this.btnCancel = new System.Windows.Forms.Button();
            this.btnRecord = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(273, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "These are the CDs/DVDs that are about to be recorded:";
            // 
            // lvCD
            // 
            this.lvCD.CheckBoxes = true;
            this.lvCD.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.colName,
            this.colSongs,
            this.colSize});
            this.lvCD.Location = new System.Drawing.Point(15, 25);
            this.lvCD.Name = "lvCD";
            this.lvCD.Size = new System.Drawing.Size(273, 143);
            this.lvCD.TabIndex = 1;
            this.lvCD.UseCompatibleStateImageBehavior = false;
            this.lvCD.View = System.Windows.Forms.View.Details;
            // 
            // colName
            // 
            this.colName.Text = "Name";
            this.colName.Width = 130;
            // 
            // colSongs
            // 
            this.colSongs.Text = "Songs";
            // 
            // colSize
            // 
            this.colSize.Text = "Size (MB)";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 180);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(150, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Free hard disk space required:";
            // 
            // lblRequiredSpace
            // 
            this.lblRequiredSpace.AutoSize = true;
            this.lblRequiredSpace.Location = new System.Drawing.Point(12, 202);
            this.lblRequiredSpace.Name = "lblRequiredSpace";
            this.lblRequiredSpace.Size = new System.Drawing.Size(185, 13);
            this.lblRequiredSpace.TabIndex = 3;
            this.lblRequiredSpace.Text = "Minimum: 0 MB Recommended: 0 MB";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 229);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(94, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "Recording device:";
            // 
            // cbDevices
            // 
            this.cbDevices.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbDevices.FormattingEnabled = true;
            this.cbDevices.Location = new System.Drawing.Point(15, 245);
            this.cbDevices.Name = "cbDevices";
            this.cbDevices.Size = new System.Drawing.Size(270, 21);
            this.cbDevices.TabIndex = 5;
            // 
            // btnCancel
            // 
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(213, 272);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.TabIndex = 6;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            // 
            // btnRecord
            // 
            this.btnRecord.Location = new System.Drawing.Point(132, 272);
            this.btnRecord.Name = "btnRecord";
            this.btnRecord.Size = new System.Drawing.Size(75, 23);
            this.btnRecord.TabIndex = 7;
            this.btnRecord.Text = "Record";
            this.btnRecord.UseVisualStyleBackColor = true;
            this.btnRecord.Click += new System.EventHandler(this.btnRecord_Click);
            // 
            // RecordForm
            // 
            this.AcceptButton = this.btnRecord;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btnCancel;
            this.ClientSize = new System.Drawing.Size(300, 304);
            this.Controls.Add(this.btnRecord);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.cbDevices);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.lblRequiredSpace);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.lvCD);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "RecordForm";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.Text = "Record to CD/DVD";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ListView lvCD;
        private System.Windows.Forms.ColumnHeader colName;
        private System.Windows.Forms.ColumnHeader colSongs;
        private System.Windows.Forms.ColumnHeader colSize;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label lblRequiredSpace;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ComboBox cbDevices;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Button btnRecord;
    }
}