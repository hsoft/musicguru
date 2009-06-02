using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using HS.Controls.Tree;
using HS.Controls.Tree.NodeControls;

namespace musicGuru
{
    public partial class IgnoreBox : Form
    {
        public IgnoreBox()
        {
            InitializeComponent();
            tvIgnoreBox.Model = new NodeModel(Program.App.Board.IgnoreBox);
            ncIcon.ValueNeeded += ncIcon_ValueNeeded;
        }

        private void ncIcon_ValueNeeded(object sender, NodeControlValueEventArgs e)
        {
            Node node = (Node)e.Node.Tag;
            Bitmap bmp = (Bitmap)Properties.Resources.ResourceManager.GetObject(node.ImageName);
            bmp.MakeTransparent(Color.Fuchsia);
            e.Value = bmp;
        }

        private void tvIgnoreBox_ItemDrag(object sender, ItemDragEventArgs e)
        {
            tvIgnoreBox.DoDragDropSelectedNodes(DragDropEffects.Move);
        }

        private void tvIgnoreBox_DragOver(object sender, DragEventArgs e)
        {
            TreeNodeAdv[] nodes = e.Data.GetData(typeof(TreeNodeAdv[])) as TreeNodeAdv[];
            if (nodes.Length > 0)
                e.Effect = e.AllowedEffect;
        }

        private void tvIgnoreBox_DragDrop(object sender, DragEventArgs e)
        {
            TreeNodeAdv[] nodes = (TreeNodeAdv[])e.Data.GetData(typeof(TreeNodeAdv[]));
            Node dropNode;
            if (tvIgnoreBox.DropPosition.Node == null)
                dropNode = Program.App.Board.IgnoreBox;
            else
            {
                dropNode = tvIgnoreBox.DropPosition.Node.Tag as Node;
                if ((tvIgnoreBox.DropPosition.Position != NodePosition.Inside) || (!dropNode.IsContainer))
                    dropNode = dropNode.Parent;
            }
            tvIgnoreBox.BeginUpdate();
            foreach (TreeNodeAdv node in nodes)
                (node.Tag as Node).Move(dropNode);
            tvIgnoreBox.EndUpdate();
        }
    }
}