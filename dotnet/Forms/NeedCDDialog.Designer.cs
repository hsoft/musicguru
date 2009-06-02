namespace musicGuru
{
    partial class NeedCDDialog
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
            this.label1 = new System.Windows.Forms.Label();
            this.lblCDName = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.lbDrives = new System.Windows.Forms.ListBox();
            this.btnOk = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.tmr = new System.Windows.Forms.Timer(this.components);
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(244, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "musicGuru needs you to insert a CD/DVD labeled:";
            // 
            // lblCDName
            // 
            this.lblCDName.AutoSize = true;
            this.lblCDName.Location = new System.Drawing.Point(12, 31);
            this.lblCDName.Name = "lblCDName";
            this.lblCDName.Size = new System.Drawing.Size(57, 13);
            this.lblCDName.TabIndex = 1;
            this.lblCDName.Text = "(CD name)";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 53);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(241, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Insert the CD in your drive, select it, and click OK.";
            // 
            // lbDrives
            // 
            this.lbDrives.FormattingEnabled = true;
            this.lbDrives.Location = new System.Drawing.Point(12, 78);
            this.lbDrives.Name = "lbDrives";
            this.lbDrives.Size = new System.Drawing.Size(244, 69);
            this.lbDrives.TabIndex = 3;
            this.lbDrives.SelectedIndexChanged += new System.EventHandler(this.lbDrives_SelectedIndexChanged);
            // 
            // btnOk
            // 
            this.btnOk.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnOk.Enabled = false;
            this.btnOk.Location = new System.Drawing.Point(100, 153);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(75, 23);
            this.btnOk.TabIndex = 4;
            this.btnOk.Text = "OK";
            this.btnOk.UseVisualStyleBackColor = true;
            // 
            // btnCancel
            // 
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(181, 153);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.TabIndex = 5;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            // 
            // tmr
            // 
            this.tmr.Enabled = true;
            this.tmr.Interval = 3000;
            this.tmr.Tick += new System.EventHandler(this.tmr_Tick);
            // 
            // NeedCDDialog
            // 
            this.AcceptButton = this.btnOk;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btnCancel;
            this.ClientSize = new System.Drawing.Size(269, 188);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.lbDrives);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.lblCDName);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "NeedCDDialog";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "CD/DVD Needed";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lblCDName;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ListBox lbDrives;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Timer tmr;
    }
}