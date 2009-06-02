using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using HS.Controls.Tree.Base;

namespace musicGuru
{
    class NodeModel : BaseTreeModel
    {
        private Node _node;

        public NodeModel(Node node)
        {
            _node = node;
            _node.Changed += Node_Changed;
        }

        private void Node_Changed(object sender, EventArgs e)
        {
            Node node = (Node)sender;
            List<Node>path = new List<Node>();
            while (node != _node)
            {
                path.Add(node);
                node = node.Parent;
            }
            path.Reverse();
            OnStructureChanged(new TreePathEventArgs(new TreePath(path.ToArray())));
        }

        #region BaseTreeModel Members

        public override IEnumerable GetChildren(TreePath treePath)
        {
            if (treePath.IsEmpty())
                return _node.Nodes;
            else
                return (treePath.LastNode as Node).Nodes;
        }

        public override int GetChildrenCount(TreePath treePath)
        {
            Node node;
            if (treePath.IsEmpty())
                node = _node;
            else
                node = treePath.LastNode as Node;
            return node.Nodes.Count;
        }

        #endregion
    }
}
