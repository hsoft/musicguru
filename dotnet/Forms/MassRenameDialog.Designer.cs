namespace musicGuru
{
    partial class MassRenameDialog
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
            this.gbNamingModel = new System.Windows.Forms.GroupBox();
            this.txtCustomModel = new System.Windows.Forms.TextBox();
            this.rbCustomModel = new System.Windows.Forms.RadioButton();
            this.rbModel4 = new System.Windows.Forms.RadioButton();
            this.rbModel3 = new System.Windows.Forms.RadioButton();
            this.rbModel2 = new System.Windows.Forms.RadioButton();
            this.rbModel1 = new System.Windows.Forms.RadioButton();
            this.gbWhitespaces = new System.Windows.Forms.GroupBox();
            this.rbWS3 = new System.Windows.Forms.RadioButton();
            this.rbWS2 = new System.Windows.Forms.RadioButton();
            this.rbWS1 = new System.Windows.Forms.RadioButton();
            this.gbExample = new System.Windows.Forms.GroupBox();
            this.lblAfter = new System.Windows.Forms.Label();
            this.lblBefore = new System.Windows.Forms.Label();
            this.btnChangeExample = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.btnCancel = new System.Windows.Forms.Button();
            this.btnOk = new System.Windows.Forms.Button();
            this.gbNamingModel.SuspendLayout();
            this.gbWhitespaces.SuspendLayout();
            this.gbExample.SuspendLayout();
            this.SuspendLayout();
            // 
            // gbNamingModel
            // 
            this.gbNamingModel.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.gbNamingModel.Controls.Add(this.txtCustomModel);
            this.gbNamingModel.Controls.Add(this.rbCustomModel);
            this.gbNamingModel.Controls.Add(this.rbModel4);
            this.gbNamingModel.Controls.Add(this.rbModel3);
            this.gbNamingModel.Controls.Add(this.rbModel2);
            this.gbNamingModel.Controls.Add(this.rbModel1);
            this.gbNamingModel.Location = new System.Drawing.Point(13, 13);
            this.gbNamingModel.Name = "gbNamingModel";
            this.gbNamingModel.Size = new System.Drawing.Size(389, 141);
            this.gbNamingModel.TabIndex = 0;
            this.gbNamingModel.TabStop = false;
            this.gbNamingModel.Text = "Select the naming model you want to use";
            // 
            // txtCustomModel
            // 
            this.txtCustomModel.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.txtCustomModel.Enabled = false;
            this.txtCustomModel.Location = new System.Drawing.Point(28, 116);
            this.txtCustomModel.Name = "txtCustomModel";
            this.txtCustomModel.Size = new System.Drawing.Size(355, 20);
            this.txtCustomModel.TabIndex = 5;
            this.txtCustomModel.Text = "%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%";
            this.txtCustomModel.TextChanged += new System.EventHandler(this.txtCustomModel_TextChanged);
            // 
            // rbCustomModel
            // 
            this.rbCustomModel.AutoSize = true;
            this.rbCustomModel.Location = new System.Drawing.Point(7, 116);
            this.rbCustomModel.Name = "rbCustomModel";
            this.rbCustomModel.Size = new System.Drawing.Size(14, 13);
            this.rbCustomModel.TabIndex = 4;
            this.rbCustomModel.Tag = "4";
            this.rbCustomModel.UseVisualStyleBackColor = true;
            this.rbCustomModel.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbModel4
            // 
            this.rbModel4.AutoSize = true;
            this.rbModel4.Location = new System.Drawing.Point(7, 92);
            this.rbModel4.Name = "rbModel4";
            this.rbModel4.Size = new System.Drawing.Size(154, 17);
            this.rbModel4.TabIndex = 3;
            this.rbModel4.Tag = "3";
            this.rbModel4.Text = "Artist / Album - Track - Title";
            this.rbModel4.UseVisualStyleBackColor = true;
            this.rbModel4.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbModel3
            // 
            this.rbModel3.AutoSize = true;
            this.rbModel3.Location = new System.Drawing.Point(7, 68);
            this.rbModel3.Name = "rbModel3";
            this.rbModel3.Size = new System.Drawing.Size(230, 17);
            this.rbModel3.TabIndex = 2;
            this.rbModel3.Tag = "2";
            this.rbModel3.Text = "Genre / Artist /( Year ) Album / Track - Title";
            this.rbModel3.UseVisualStyleBackColor = true;
            this.rbModel3.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbModel2
            // 
            this.rbModel2.AutoSize = true;
            this.rbModel2.Location = new System.Drawing.Point(7, 44);
            this.rbModel2.Name = "rbModel2";
            this.rbModel2.Size = new System.Drawing.Size(156, 17);
            this.rbModel2.TabIndex = 1;
            this.rbModel2.Tag = "1";
            this.rbModel2.Text = "Artist / Album / Track - Title";
            this.rbModel2.UseVisualStyleBackColor = true;
            this.rbModel2.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbModel1
            // 
            this.rbModel1.AutoSize = true;
            this.rbModel1.Checked = true;
            this.rbModel1.Location = new System.Drawing.Point(7, 20);
            this.rbModel1.Name = "rbModel1";
            this.rbModel1.Size = new System.Drawing.Size(188, 17);
            this.rbModel1.TabIndex = 0;
            this.rbModel1.TabStop = true;
            this.rbModel1.Tag = "0";
            this.rbModel1.Text = "Artist / Album / Track - Artist - Title";
            this.rbModel1.UseVisualStyleBackColor = true;
            this.rbModel1.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // gbWhitespaces
            // 
            this.gbWhitespaces.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.gbWhitespaces.Controls.Add(this.rbWS3);
            this.gbWhitespaces.Controls.Add(this.rbWS2);
            this.gbWhitespaces.Controls.Add(this.rbWS1);
            this.gbWhitespaces.Location = new System.Drawing.Point(13, 161);
            this.gbWhitespaces.Name = "gbWhitespaces";
            this.gbWhitespaces.Size = new System.Drawing.Size(389, 91);
            this.gbWhitespaces.TabIndex = 1;
            this.gbWhitespaces.TabStop = false;
            this.gbWhitespaces.Text = "Dealing with whitespaces";
            // 
            // rbWS3
            // 
            this.rbWS3.AutoSize = true;
            this.rbWS3.Location = new System.Drawing.Point(7, 68);
            this.rbWS3.Name = "rbWS3";
            this.rbWS3.Size = new System.Drawing.Size(240, 17);
            this.rbWS3.TabIndex = 2;
            this.rbWS3.Tag = "2";
            this.rbWS3.Text = "Replace underscores with a space character.";
            this.rbWS3.UseVisualStyleBackColor = true;
            this.rbWS3.CheckedChanged += new System.EventHandler(this.rbWS_CheckedChanged);
            // 
            // rbWS2
            // 
            this.rbWS2.AutoSize = true;
            this.rbWS2.Location = new System.Drawing.Point(7, 44);
            this.rbWS2.Name = "rbWS2";
            this.rbWS2.Size = new System.Drawing.Size(234, 17);
            this.rbWS2.TabIndex = 1;
            this.rbWS2.Tag = "1";
            this.rbWS2.Text = "Replace whitespaces with underscores ( _ ).";
            this.rbWS2.UseVisualStyleBackColor = true;
            this.rbWS2.CheckedChanged += new System.EventHandler(this.rbWS_CheckedChanged);
            // 
            // rbWS1
            // 
            this.rbWS1.AutoSize = true;
            this.rbWS1.Checked = true;
            this.rbWS1.Location = new System.Drawing.Point(7, 20);
            this.rbWS1.Name = "rbWS1";
            this.rbWS1.Size = new System.Drawing.Size(108, 17);
            this.rbWS1.TabIndex = 0;
            this.rbWS1.TabStop = true;
            this.rbWS1.Tag = "0";
            this.rbWS1.Text = "Leave them as is.";
            this.rbWS1.UseVisualStyleBackColor = true;
            this.rbWS1.CheckedChanged += new System.EventHandler(this.rbWS_CheckedChanged);
            // 
            // gbExample
            // 
            this.gbExample.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.gbExample.Controls.Add(this.lblAfter);
            this.gbExample.Controls.Add(this.lblBefore);
            this.gbExample.Controls.Add(this.btnChangeExample);
            this.gbExample.Controls.Add(this.label2);
            this.gbExample.Controls.Add(this.label1);
            this.gbExample.Location = new System.Drawing.Point(13, 259);
            this.gbExample.Name = "gbExample";
            this.gbExample.Size = new System.Drawing.Size(389, 100);
            this.gbExample.TabIndex = 2;
            this.gbExample.TabStop = false;
            this.gbExample.Text = "Example";
            // 
            // lblAfter
            // 
            this.lblAfter.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.lblAfter.Location = new System.Drawing.Point(54, 45);
            this.lblAfter.Name = "lblAfter";
            this.lblAfter.Size = new System.Drawing.Size(329, 13);
            this.lblAfter.TabIndex = 4;
            this.lblAfter.Text = "(After)";
            // 
            // lblBefore
            // 
            this.lblBefore.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.lblBefore.Location = new System.Drawing.Point(54, 20);
            this.lblBefore.Name = "lblBefore";
            this.lblBefore.Size = new System.Drawing.Size(329, 13);
            this.lblBefore.TabIndex = 3;
            this.lblBefore.Text = "(Before)";
            // 
            // btnChangeExample
            // 
            this.btnChangeExample.Location = new System.Drawing.Point(10, 71);
            this.btnChangeExample.Name = "btnChangeExample";
            this.btnChangeExample.Size = new System.Drawing.Size(109, 23);
            this.btnChangeExample.TabIndex = 2;
            this.btnChangeExample.Text = "Change Example";
            this.btnChangeExample.UseVisualStyleBackColor = true;
            this.btnChangeExample.Click += new System.EventHandler(this.btnChangeExample_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(7, 45);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(32, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "After:";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(7, 20);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Before:";
            // 
            // btnCancel
            // 
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(327, 365);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.TabIndex = 3;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            // 
            // btnOk
            // 
            this.btnOk.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnOk.Location = new System.Drawing.Point(246, 365);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(75, 23);
            this.btnOk.TabIndex = 4;
            this.btnOk.Text = "OK";
            this.btnOk.UseVisualStyleBackColor = true;
            // 
            // MassRenameDialog
            // 
            this.AcceptButton = this.btnOk;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btnCancel;
            this.ClientSize = new System.Drawing.Size(414, 396);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.gbExample);
            this.Controls.Add(this.gbWhitespaces);
            this.Controls.Add(this.gbNamingModel);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "MassRenameDialog";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.Text = "Mass Rename";
            this.gbNamingModel.ResumeLayout(false);
            this.gbNamingModel.PerformLayout();
            this.gbWhitespaces.ResumeLayout(false);
            this.gbWhitespaces.PerformLayout();
            this.gbExample.ResumeLayout(false);
            this.gbExample.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox gbNamingModel;
        private System.Windows.Forms.RadioButton rbCustomModel;
        private System.Windows.Forms.RadioButton rbModel4;
        private System.Windows.Forms.RadioButton rbModel3;
        private System.Windows.Forms.RadioButton rbModel2;
        private System.Windows.Forms.RadioButton rbModel1;
        private System.Windows.Forms.TextBox txtCustomModel;
        private System.Windows.Forms.GroupBox gbWhitespaces;
        private System.Windows.Forms.RadioButton rbWS3;
        private System.Windows.Forms.RadioButton rbWS2;
        private System.Windows.Forms.RadioButton rbWS1;
        private System.Windows.Forms.GroupBox gbExample;
        private System.Windows.Forms.Button btnChangeExample;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.Label lblAfter;
        private System.Windows.Forms.Label lblBefore;
    }
}