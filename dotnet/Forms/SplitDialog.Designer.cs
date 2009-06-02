namespace musicGuru
{
    partial class SplitDialog
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
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.txtCustomModel = new System.Windows.Forms.TextBox();
            this.rbCustomModel = new System.Windows.Forms.RadioButton();
            this.rbLetter = new System.Windows.Forms.RadioButton();
            this.rbName = new System.Windows.Forms.RadioButton();
            this.rbSequence = new System.Windows.Forms.RadioButton();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.numCapacity = new System.Windows.Forms.NumericUpDown();
            this.rbCustomCapacity = new System.Windows.Forms.RadioButton();
            this.rb8500 = new System.Windows.Forms.RadioButton();
            this.rb4700 = new System.Windows.Forms.RadioButton();
            this.rb700 = new System.Windows.Forms.RadioButton();
            this.tbGroupLevel = new System.Windows.Forms.TrackBar();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.lblExample = new System.Windows.Forms.Label();
            this.btnChangeExample = new System.Windows.Forms.Button();
            this.cbTruncate = new System.Windows.Forms.CheckBox();
            this.btnOk = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numCapacity)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbGroupLevel)).BeginInit();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.txtCustomModel);
            this.groupBox1.Controls.Add(this.rbCustomModel);
            this.groupBox1.Controls.Add(this.rbLetter);
            this.groupBox1.Controls.Add(this.rbName);
            this.groupBox1.Controls.Add(this.rbSequence);
            this.groupBox1.Location = new System.Drawing.Point(13, 13);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(230, 118);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Select the naming model you want to use";
            // 
            // txtCustomModel
            // 
            this.txtCustomModel.Enabled = false;
            this.txtCustomModel.Location = new System.Drawing.Point(28, 92);
            this.txtCustomModel.Name = "txtCustomModel";
            this.txtCustomModel.Size = new System.Drawing.Size(193, 20);
            this.txtCustomModel.TabIndex = 4;
            this.txtCustomModel.Text = "CD %item:first:3% - %item:last:3%";
            // 
            // rbCustomModel
            // 
            this.rbCustomModel.AutoSize = true;
            this.rbCustomModel.Location = new System.Drawing.Point(7, 92);
            this.rbCustomModel.Name = "rbCustomModel";
            this.rbCustomModel.Size = new System.Drawing.Size(14, 13);
            this.rbCustomModel.TabIndex = 3;
            this.rbCustomModel.Tag = "3";
            this.rbCustomModel.UseVisualStyleBackColor = true;
            this.rbCustomModel.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbLetter
            // 
            this.rbLetter.AutoSize = true;
            this.rbLetter.Location = new System.Drawing.Point(7, 68);
            this.rbLetter.Name = "rbLetter";
            this.rbLetter.Size = new System.Drawing.Size(175, 17);
            this.rbLetter.TabIndex = 2;
            this.rbLetter.Tag = "2";
            this.rbLetter.Text = "CD <First Letter> - <Last Letter>";
            this.rbLetter.UseVisualStyleBackColor = true;
            this.rbLetter.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbName
            // 
            this.rbName.AutoSize = true;
            this.rbName.Location = new System.Drawing.Point(7, 44);
            this.rbName.Name = "rbName";
            this.rbName.Size = new System.Drawing.Size(177, 17);
            this.rbName.TabIndex = 1;
            this.rbName.Tag = "1";
            this.rbName.Text = "CD <First Name> - <Last Name>";
            this.rbName.UseVisualStyleBackColor = true;
            this.rbName.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // rbSequence
            // 
            this.rbSequence.AutoSize = true;
            this.rbSequence.Checked = true;
            this.rbSequence.Location = new System.Drawing.Point(7, 20);
            this.rbSequence.Name = "rbSequence";
            this.rbSequence.Size = new System.Drawing.Size(104, 17);
            this.rbSequence.TabIndex = 0;
            this.rbSequence.TabStop = true;
            this.rbSequence.Tag = "0";
            this.rbSequence.Text = "CD <Sequence>";
            this.rbSequence.UseVisualStyleBackColor = true;
            this.rbSequence.CheckedChanged += new System.EventHandler(this.rbModel_CheckedChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.numCapacity);
            this.groupBox2.Controls.Add(this.rbCustomCapacity);
            this.groupBox2.Controls.Add(this.rb8500);
            this.groupBox2.Controls.Add(this.rb4700);
            this.groupBox2.Controls.Add(this.rb700);
            this.groupBox2.Location = new System.Drawing.Point(250, 13);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(200, 118);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "CD/DVD capacity";
            // 
            // numCapacity
            // 
            this.numCapacity.Enabled = false;
            this.numCapacity.Increment = new decimal(new int[] {
            50,
            0,
            0,
            0});
            this.numCapacity.Location = new System.Drawing.Point(102, 92);
            this.numCapacity.Maximum = new decimal(new int[] {
            99999,
            0,
            0,
            0});
            this.numCapacity.Name = "numCapacity";
            this.numCapacity.Size = new System.Drawing.Size(69, 20);
            this.numCapacity.TabIndex = 4;
            this.numCapacity.Value = new decimal(new int[] {
            650,
            0,
            0,
            0});
            this.numCapacity.ValueChanged += new System.EventHandler(this.numCapacity_ValueChanged);
            // 
            // rbCustomCapacity
            // 
            this.rbCustomCapacity.AutoSize = true;
            this.rbCustomCapacity.Location = new System.Drawing.Point(7, 92);
            this.rbCustomCapacity.Name = "rbCustomCapacity";
            this.rbCustomCapacity.Size = new System.Drawing.Size(88, 17);
            this.rbCustomCapacity.TabIndex = 3;
            this.rbCustomCapacity.Tag = "3";
            this.rbCustomCapacity.Text = "Custom (MB):";
            this.rbCustomCapacity.UseVisualStyleBackColor = true;
            this.rbCustomCapacity.CheckedChanged += new System.EventHandler(this.rbCapacity_CheckedChanged);
            // 
            // rb8500
            // 
            this.rb8500.AutoSize = true;
            this.rb8500.Location = new System.Drawing.Point(7, 68);
            this.rb8500.Name = "rb8500";
            this.rb8500.Size = new System.Drawing.Size(150, 17);
            this.rb8500.TabIndex = 2;
            this.rb8500.Tag = "2";
            this.rb8500.Text = "8.5 GB (double layer DVD)";
            this.rb8500.UseVisualStyleBackColor = true;
            this.rb8500.CheckedChanged += new System.EventHandler(this.rbCapacity_CheckedChanged);
            // 
            // rb4700
            // 
            this.rb4700.AutoSize = true;
            this.rb4700.Location = new System.Drawing.Point(7, 44);
            this.rb4700.Name = "rb4700";
            this.rb4700.Size = new System.Drawing.Size(145, 17);
            this.rb4700.TabIndex = 1;
            this.rb4700.Tag = "1";
            this.rb4700.Text = "4.7 GB (single layer DVD)";
            this.rb4700.UseVisualStyleBackColor = true;
            this.rb4700.CheckedChanged += new System.EventHandler(this.rbCapacity_CheckedChanged);
            // 
            // rb700
            // 
            this.rb700.AutoSize = true;
            this.rb700.Checked = true;
            this.rb700.Location = new System.Drawing.Point(7, 20);
            this.rb700.Name = "rb700";
            this.rb700.Size = new System.Drawing.Size(86, 17);
            this.rb700.TabIndex = 0;
            this.rb700.TabStop = true;
            this.rb700.Tag = "0";
            this.rb700.Text = "700 MB (CD)";
            this.rb700.UseVisualStyleBackColor = true;
            this.rb700.CheckedChanged += new System.EventHandler(this.rbCapacity_CheckedChanged);
            // 
            // tbGroupLevel
            // 
            this.tbGroupLevel.Location = new System.Drawing.Point(12, 159);
            this.tbGroupLevel.Maximum = 5;
            this.tbGroupLevel.Name = "tbGroupLevel";
            this.tbGroupLevel.Size = new System.Drawing.Size(104, 45);
            this.tbGroupLevel.TabIndex = 2;
            this.tbGroupLevel.Scroll += new System.EventHandler(this.tbGroupLevel_Scroll);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(10, 143);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(75, 13);
            this.label1.TabIndex = 3;
            this.label1.Text = "Grouping level";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(145, 143);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(255, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Folders on the same level as this one will be grouped";
            // 
            // lblExample
            // 
            this.lblExample.Location = new System.Drawing.Point(145, 165);
            this.lblExample.Name = "lblExample";
            this.lblExample.Size = new System.Drawing.Size(305, 17);
            this.lblExample.TabIndex = 5;
            this.lblExample.Text = "(no grouping)";
            // 
            // btnChangeExample
            // 
            this.btnChangeExample.Location = new System.Drawing.Point(148, 185);
            this.btnChangeExample.Name = "btnChangeExample";
            this.btnChangeExample.Size = new System.Drawing.Size(95, 23);
            this.btnChangeExample.TabIndex = 3;
            this.btnChangeExample.Text = "Change Example";
            this.btnChangeExample.UseVisualStyleBackColor = true;
            this.btnChangeExample.Click += new System.EventHandler(this.btnChangeExample_Click);
            // 
            // cbTruncate
            // 
            this.cbTruncate.AutoSize = true;
            this.cbTruncate.Checked = true;
            this.cbTruncate.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbTruncate.Location = new System.Drawing.Point(12, 211);
            this.cbTruncate.Name = "cbTruncate";
            this.cbTruncate.Size = new System.Drawing.Size(332, 17);
            this.cbTruncate.TabIndex = 4;
            this.cbTruncate.Text = "Truncate names to 16 characters (This is the max for CD names.)";
            this.cbTruncate.UseVisualStyleBackColor = true;
            this.cbTruncate.CheckedChanged += new System.EventHandler(this.cbTruncate_CheckedChanged);
            // 
            // btnOk
            // 
            this.btnOk.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnOk.Location = new System.Drawing.Point(294, 234);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(75, 23);
            this.btnOk.TabIndex = 5;
            this.btnOk.Text = "OK";
            this.btnOk.UseVisualStyleBackColor = true;
            // 
            // btnCancel
            // 
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(375, 234);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.TabIndex = 6;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            // 
            // SplitDialog
            // 
            this.AcceptButton = this.btnOk;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.btnCancel;
            this.ClientSize = new System.Drawing.Size(463, 270);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.cbTruncate);
            this.Controls.Add(this.btnChangeExample);
            this.Controls.Add(this.lblExample);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tbGroupLevel);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "SplitDialog";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.Text = "Split to CD/DVD";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numCapacity)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbGroupLevel)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.RadioButton rbCustomModel;
        private System.Windows.Forms.RadioButton rbLetter;
        private System.Windows.Forms.RadioButton rbName;
        private System.Windows.Forms.RadioButton rbSequence;
        private System.Windows.Forms.TextBox txtCustomModel;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.NumericUpDown numCapacity;
        private System.Windows.Forms.RadioButton rbCustomCapacity;
        private System.Windows.Forms.RadioButton rb8500;
        private System.Windows.Forms.RadioButton rb4700;
        private System.Windows.Forms.RadioButton rb700;
        private System.Windows.Forms.TrackBar tbGroupLevel;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label lblExample;
        private System.Windows.Forms.Button btnChangeExample;
        private System.Windows.Forms.CheckBox cbTruncate;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.Button btnCancel;
    }
}