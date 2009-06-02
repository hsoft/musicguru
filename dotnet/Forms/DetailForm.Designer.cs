namespace musicGuru
{
    partial class DetailForm
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
            this.lvInfo = new System.Windows.Forms.ListView();
            this.colName = new System.Windows.Forms.ColumnHeader();
            this.colValue = new System.Windows.Forms.ColumnHeader();
            this.SuspendLayout();
            // 
            // lvInfo
            // 
            this.lvInfo.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.colName,
            this.colValue});
            this.lvInfo.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lvInfo.FullRowSelect = true;
            this.lvInfo.Location = new System.Drawing.Point(0, 0);
            this.lvInfo.MultiSelect = false;
            this.lvInfo.Name = "lvInfo";
            this.lvInfo.Size = new System.Drawing.Size(284, 192);
            this.lvInfo.TabIndex = 0;
            this.lvInfo.UseCompatibleStateImageBehavior = false;
            this.lvInfo.View = System.Windows.Forms.View.Details;
            // 
            // colName
            // 
            this.colName.Text = "Name";
            this.colName.Width = 80;
            // 
            // colValue
            // 
            this.colValue.Text = "Value";
            this.colValue.Width = 200;
            // 
            // DetailForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(284, 192);
            this.Controls.Add(this.lvInfo);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.SizableToolWindow;
            this.Name = "DetailForm";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.Manual;
            this.Text = "Selection Details";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ListView lvInfo;
        private System.Windows.Forms.ColumnHeader colName;
        private System.Windows.Forms.ColumnHeader colValue;
    }
}