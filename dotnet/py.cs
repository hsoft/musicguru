using System;
using System.Collections.Generic;
using System.Collections;
using System.Text;
using Python.Runtime;
using HS.Dialogs;
using HS.Controls.Tree.Base;

namespace musicGuru
{
    public class Py
    {
        private IntPtr _gil;
        internal PyObject _py;

        public Py(PyObject pyRef)
        {
            _py = pyRef;
        }

        protected void _Lock()
        {
            _gil = PythonEngine.AcquireLock();
        }

        protected void _Unlock()
        {
            PythonEngine.ReleaseLock(_gil);
        }
    }

    public class Node : Py
    {
        public Node(PyObject pyRef, Node parent)
            : base(pyRef)
        {
            _parent = null;
            Parent = parent;
        }

        #region Static

        static private Dictionary<int,Node> _cached = new Dictionary<int,Node>();
        static public Node GetNode(PyObject pyRef, Node parent)
        {
            if (_cached.ContainsKey(pyRef.Handle.ToInt32()))
                return _cached[pyRef.Handle.ToInt32()];
            else
            {
                Node result = new Node(pyRef,parent);
                _cached[pyRef.Handle.ToInt32()] = result;
                return result;
            }
        }

        static public void ClearNodeCache()
        {
            _cached.Clear();
        }

        #endregion

        #region Properties

        private Node _parent = null;
        public Node Parent
        {
            get { return _parent; }
            set
            {
                if (value == _parent)
                    return;
                if (_parent != null)
                    Changed -= _parent.Children_Changed;
                _parent = value;
                if (_parent != null)
                    Changed += _parent.Children_Changed;
            }
        }

        private ListGenerator<PyObject, Node> _nodes = null;
        public ListGenerator<PyObject, Node> Nodes
        {
            get
            {
                if (_nodes == null)
                {
                    _Lock();
                    _nodes = new ListGenerator<PyObject, Node>(_EnumerateChildren(), _py.Length(), _GenerateNode);
                    _Unlock();
                }
                return _nodes;
            }
        }

        private int _isContainer = -1;
        public bool IsContainer
        {
            get
            {
                if (_isContainer < 0)
                {
                    _Lock();
                    _isContainer = PyInt.AsInt(_py.GetAttr("is_container")).ToInt32();
                    _Unlock();
                }
                return _isContainer > 0;
            }
        }

        public string PhysicalPath
        {
            get
            {
                _Lock();
                PyObject pyOriginal = _py.GetAttr("original");
                PyObject pyPath = pyOriginal.GetAttr("physical_path");
                PyObject pyResult = pyPath.InvokeMethod("__unicode__");
                _Unlock();
                return pyResult.ToString();
            }
        }

        private List<string> _data = null;
        public List<string> data
        {
            get
            {
                if (_data == null)
                    _data = Program.App.GetNodeData(this);
                return _data;
            }
        }

        public string Name 
        { 
            get { return data[0]; }
            set 
            {
                Program.App.RenameNode(this, value);
                _data = null;
                //If it results in a directory merge, we must invalidate parent.
                PyObject pyParent = _py.GetAttr("parent");
                if (pyParent == PyObject.FromManagedObject(null))
                {
                    foreach (Node node in Parent.Nodes)
                        node.Invalidate();
                    Parent.OnChanged();
                }
            }
        }
        public string Location { get { return data[1]; } }
        public string Songs { get { return data[2]; } }
        public string Size { get { return data[3]; } }
        public string Time { get { return data[4]; } }
        public string ImageName { get { return data[5]; } }

        #endregion

        #region Private

        private IEnumerator _EnumerateChildren()
        {
            foreach (PyObject directory in PyList.AsList(_py.GetAttr("dirs")))
                yield return directory;
            foreach (PyObject song in PyList.AsList(_py.GetAttr("files")))
                yield return song;
        }

        private void _GenerateNode(PyObject source, out Node result)
        {
            result = Node.GetNode(source,this);
        }

        #endregion

        public void Invalidate()
        {
            _nodes = null;
            _data = null;
        }

        public void Move(Node destination)
        {
            if (destination == Parent)
                return;
            if (!destination.IsContainer)
                return;
            _Lock();
            _py.InvokeMethod("Move", destination._py);
            _Unlock();
            Parent.OnChanged();
            Parent = destination;
            Parent.OnChanged();
            _data = null;
        }

        public Node NewFolder()
        {
            _Lock();
            PyObject result = _py.InvokeMethod("NewDirectory", new PyString("New Folder"));
            _Unlock();
            OnChanged();
            return Node.GetNode(result, this);
        }

        public event EventHandler Changed;
        internal void OnChanged()
        {
            Invalidate();
            if (Changed != null)
                Changed(this, EventArgs.Empty);
        }

        private void Children_Changed(object sender, EventArgs e)
        {
            if (Changed != null)
                Changed(sender, e);
        }
    }

    public class Location : Py
    {
        public Location(PyObject pyRef)
            : base(pyRef)
        {
        }

        #region Properties

        private List<string> _data = null;
        public List<string> data
        {
            get
            {
                if (_data == null)
                    _data = Program.App.GetLocationData(this);
                return _data;
            }
        }

        public string Name { get { return data[0]; } }
        public string Songs { get { return data[1]; } }
        public string Size { get { return data[2]; } }
        public bool IsRemovable { get { return data[3] == "True"; } }
        public bool IsAvailable { get { return data[4] == "True"; } }
        public string Path { 
            get { return data[5]; }
            set
            {
                _Lock();
                _py.SetAttr("initial_path", new PyString(value));
                _Unlock();
            }
        }

        #endregion

        public void RemoveFromBoard()
        {
            Program.App.Board.RemoveLocation(this);
        }

        public void RemoveFromCollection()
        {
            RemoveFromBoard();
            _Lock();
            _py.InvokeMethod("delete");
            _Unlock();
        }

        public void Toggle()
        {
            Program.App.Board.ToggleLocation(this);
        }
    }

    public class Board : Node
    {
        public Board(PyObject pyRef) : base(pyRef,null)
        {
        }

        private Node _ignoreBox = null;
        public Node IgnoreBox
        {
            get
            {
                if (_ignoreBox == null)
                {
                    _Lock();
                    PyObject pyIgnoreBox = _py.GetAttr("ignore_box");
                    _Unlock();
                    _ignoreBox = new Node(pyIgnoreBox,null);
                }
                return _ignoreBox;
            }
        }

        public bool Splitted
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("splitted"));
                _Unlock();
                return result.ToInt32() != 0;
            }
        }

        public bool ContainsLocation(Location location)
        {
            _Lock();
            PyList locations = PyList.AsList(_py.GetAttr("locations"));
            bool result = locations.Contains(location._py);
            _Unlock();
            return result;
        }

        public void Empty()
        {
            _Lock();
            _py.InvokeMethod("Empty");
            _Unlock();
            Node.ClearNodeCache();
            OnChanged();
        }

        public void MoveConflicts(bool withOriginals)
        {
            _Lock();
            PyInt pyWithOriginal = new PyInt(Convert.ToByte(withOriginals));
            _py.InvokeMethod("MoveConflicts", pyWithOriginal);
            _Unlock();
            Node.ClearNodeCache();
            OnChanged();
            IgnoreBox.OnChanged();
        }

        public void RemoveLocation(Location location)
        {
            _Lock();
            _py.InvokeMethod("RemoveLocation", location._py);
            _Unlock();
            OnChanged();
        }

        public void ToggleLocation(Location location)
        {
            _Lock();
            _py.InvokeMethod("ToggleLocation", location._py);
            _Unlock();
            OnChanged();
            IgnoreBox.OnChanged();
        }
    }

    public class MassRenamePanel : Py
    {
        public MassRenamePanel(PyObject pyRef) : base(pyRef)
        {
        }

        #region Properties

        public int ModelIndex
        {
            get 
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("model_index"));
                _Unlock();
                return result.ToInt32();
            }
            set 
            {
                _Lock();
                _py.SetAttr("model_index", new PyInt(value));
                _Unlock();
            }
        }

        public int WhitespaceIndex
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("whitespace_index"));
                _Unlock();
                return result.ToInt32();
            }
            set
            {
                _Lock();
                _py.SetAttr("whitespace_index", new PyInt(value));
                _Unlock();
            }
        }

        public string CustomModel
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("custom_model");
                _Unlock();
                return result.ToString();
            }
            set
            {
                _Lock();
                _py.SetAttr("custom_model", new PyString(value));
                _Unlock();
            }
        }

        public string ExampleBefore
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("example_before");
                _Unlock();
                return result.ToString();
            }
        }

        public string ExampleAfter
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("example_after");
                _Unlock();
                return result.ToString();
            }
        }

        public string Model
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("model");
                _Unlock();
                return result.ToString();
            }
        }

        public int Whitespace
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("whitespace");
                _Unlock();
                return PyInt.AsInt(result).ToInt32();
            }
        }

        #endregion

        public void ChangeExample()
        {
            _Lock();
            _py.InvokeMethod("ChangeExample");
            _Unlock();
        }
    }

    public class SplitPanel : Py
    {
        public SplitPanel(PyObject pyRef) : base(pyRef)
        {
        }

        #region Properties

        public int ModelIndex
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("model_index"));
                _Unlock();
                return result.ToInt32();
            }
            set
            {
                _Lock();
                _py.SetAttr("model_index", new PyInt(value));
                _Unlock();
            }
        }

        public int CapacityIndex
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("capacity_index"));
                _Unlock();
                return result.ToInt32();
            }
            set
            {
                _Lock();
                _py.SetAttr("capacity_index", new PyInt(value));
                _Unlock();
            }
        }

        public int GroupingLevel
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("grouping_level"));
                _Unlock();
                return result.ToInt32();
            }
            set
            {
                _Lock();
                _py.SetAttr("grouping_level", new PyInt(value));
                _Unlock();
            }
        }

        public long CustomCapacity
        {
            get
            {
                _Lock();
                PyLong result = PyLong.AsLong(_py.GetAttr("custom_capacity"));
                _Unlock();
                return result.ToInt64();
            }
            set
            {
                _Lock();
                _py.SetAttr("custom_capacity", new PyInt(value));
                _Unlock();
            }
        }

        public int TruncateNameTo
        {
            get
            {
                _Lock();
                PyInt result = PyInt.AsInt(_py.GetAttr("truncate_name_to"));
                _Unlock();
                return result.ToInt32();
            }
            set
            {
                _Lock();
                _py.SetAttr("truncate_name_to", new PyInt(value));
                _Unlock();
            }
        }

        public string Example
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("example");
                _Unlock();
                return result.ToString();
            }
        }

        public string Model
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("model");
                _Unlock();
                return result.ToString();
            }
        }

        public long Capacity
        {
            get
            {
                _Lock();
                PyObject result = _py.GetAttr("capacity");
                _Unlock();
                return PyLong.AsLong(result).ToInt64();
            }
        }

        #endregion

        public void ChangeExample()
        {
            _Lock();
            _py.InvokeMethod("ChangeExample");
            _Unlock();
        }
    }

    public class App : Py
    {
        public App(PyObject pyRef)
            : base(pyRef)
        {
            _Lock();
            _board = new Board(_py.GetAttr("board"));
            _Unlock();
        }

        private Board _board;
        public Board Board
        {
            get { return _board; }
        }

        public int MinimumFreeBytes
        {
            get
            {
                _Lock();
                PyObject pyBuffer = _py.GetAttr("buffer");
                PyInt pyResult = PyInt.AsInt(pyBuffer.InvokeMethod("GetMinimumBytesRequired"));
                _Unlock();
                return pyResult.ToInt32();
            }
        }

        public int RecommendedFreeBytes
        {
            get
            {
                _Lock();
                PyObject pyBuffer = _py.GetAttr("buffer");
                PyInt pyResult = PyInt.AsInt(pyBuffer.InvokeMethod("GetMaximumBytesRequired"));
                _Unlock();
                return pyResult.ToInt32();
            }
        }

        public int AddLocation(ProgressCallback callback, params object[] p)
        {
            _Lock();
            PyString pyPath = new PyString((string)p[0]);
            PyString pyName = new PyString((string)p[1]);
            PyInt pyRemoveable = new PyInt(Convert.ToByte((bool)p[2]));
            _py.InvokeMethod("AddLocation", pyPath, pyName, pyRemoveable, PyObject.FromManagedObject(callback));
            _Unlock();
            return 0;
        }

        public string CanAddLocation(string path, string name)
        {
            _Lock();
            string result = _py.InvokeMethod("CanAddLocation", new PyString(path), new PyString(name)).ToString();
            _Unlock();
            return result;
        }

        public MassRenamePanel GetMassRenamePanel()
        {
            _Lock();
            PyObject panel = _py.InvokeMethod("GetMassRenamePanel");
            _Unlock();
            return new MassRenamePanel(panel);
        }

        public SplitPanel GetSplitPanel()
        {
            _Lock();
            PyObject panel = _py.InvokeMethod("GetSplitPanel");
            _Unlock();
            return new SplitPanel(panel);
        }

        public List<string> GetNodeData(Node song)
        {
            _Lock();
            PyList pyResult = PyList.AsList(_py.InvokeMethod("GetNodeData", song._py));
            List<string> result = new List<string>();
            foreach (PyObject o in pyResult)
                result.Add(o.ToString());
            _Unlock();
            return result;
        }

        public List<string> GetLocationData(Location location)
        {
            _Lock();
            PyList pyResult = PyList.AsList(_py.InvokeMethod("GetLocationData", location._py));
            List<string> result = new List<string>();
            foreach (PyObject o in pyResult)
                result.Add(o.ToString());
            _Unlock();
            return result;
        }

        public List<Location> GetLocations()
        {
            List<Location> result = new List<Location>();
            _Lock();
            PyObject pyCollection = _py.GetAttr("collection");
            PyList pyLocations = PyList.AsList(pyCollection.GetAttr("dirs"));
            foreach (PyObject location in pyLocations)
                result.Add(new Location(location));
            _Unlock();
            return result;
        }

        public List<List<string>> GetSelectionInfo(List<Node> selection)
        {
            List<List<string>> result = new List<List<string>>();
            _Lock();
            PyList pyArgs = new PyList();
            foreach (Node song in selection)
                pyArgs.Append(song._py);
            PyList pyResult = PyList.AsList(_py.InvokeMethod("GetSelectionInfo", pyArgs));
            foreach (PyObject pyPair in pyResult)
            {
                List<string> pair = new List<string>();
                pair.Add(pyPair[0].ToString());
                pair.Add(pyPair[1].ToString());
                result.Add(pair);
            }
            _Unlock();
            return result;
        }

        public int MassRename(ProgressCallback callback, params object[] p)
        {
            _Lock();
            PyString pyModel = new PyString((string)p[0]);
            PyInt pyWhitespace = new PyInt((int)p[1]);
            _py.InvokeMethod("MassRename", pyModel, pyWhitespace, PyObject.FromManagedObject(callback));
            _Unlock();
            Node.ClearNodeCache();
            Board.OnChanged();
            return 0;
        }

        public void RemoveEmptyDirs()
        {
            _Lock();
            _py.InvokeMethod("RemoveEmptyDirs");
            _Unlock();
            Node.ClearNodeCache();
            Board.OnChanged();
        }

        public string RenameNode(Node node, string newName)
        {
            _Lock();
            PyObject result = _py.InvokeMethod("RenameNode", node._py, new PyString(newName));
            _Unlock();
            return result.ToString();
        }

        public int Split(ProgressCallback callback, params object[] p)
        {
            _Lock();
            PyString pyModel = new PyString((string)p[0]);
            PyLong pyCapacity = new PyLong((long)p[1]);
            PyInt pyGroupingLevel = new PyInt((int)p[2]);
            PyInt pyTruncateTo = new PyInt((int)p[3]);
            _py.InvokeMethod("Split", pyModel, pyCapacity, pyGroupingLevel, pyTruncateTo, PyObject.FromManagedObject(callback));
            _Unlock();
            Node.ClearNodeCache();
            Board.OnChanged();
            return 0;
        }

        public void SwitchConflictAndOriginal(Node node)
        {
            _Lock();
            PyObject pyOriginal = _py.InvokeMethod("SwitchConflictAndOriginal", node._py);
            _Unlock();
            node.Parent.OnChanged();
            node.Invalidate();
            Node.GetNode(pyOriginal, node.Parent).Invalidate();
        }

        public void Unsplit()
        {
            _Lock();
            Board._py.InvokeMethod("Unsplit");
            _Unlock();
            Board.OnChanged();
        }

        public int UpdateCollection(ProgressCallback callback, params object[] p)
        {
            _Lock();
            _py.InvokeMethod("UpdateCollection", PyObject.FromManagedObject(callback));
            _Unlock();
            return 0;
        }

        public int UpdateVolume(ProgressCallback callback, params object[] p)
        {
            _Lock();
            Location loc = (Location)p[0];
            _py.InvokeMethod("UpdateVolume", loc._py, PyObject.FromManagedObject(callback));
            _Unlock();
            return 0;
        }

        #region Materialize

        public void CleanBuffer(Node node)
        {
            _Lock();
            _py.InvokeMethod("CleanBuffer", node._py);
            _Unlock();
        }

        public int CopyOrMove(ProgressCallback callback, params object[] p)
        {
            bool copy = (bool)p[0];
            _Lock();
            PyInt pyCopy = new PyInt(Convert.ToInt32(copy));
            PyString pyDestination = new PyString((string)p[1]);
            PyObject pyCallback = PyObject.FromManagedObject(callback);
            NeedCDCallback onNeedCD = NeedCDDialog.AskForCD;
            PyObject pyOnNeedCD = PyObject.FromManagedObject(onNeedCD);
            _py.InvokeMethod("CopyOrMove", pyCopy, pyDestination, pyCallback, pyOnNeedCD);
            _Unlock();
            if (!copy)
                Board.Empty();
            return 0;
        }

        public int FetchSourceSongs(ProgressCallback callback, params object[] p)
        {
            _Lock();
            PyObject pyCD = (p[0] as Node)._py;
            PyObject pyCallback = PyObject.FromManagedObject(callback);
            NeedCDCallback onNeedCD = NeedCDDialog.AskForCD;
            PyObject pyOnNeedCD = PyObject.FromManagedObject(onNeedCD);
            _py.InvokeMethod("FetchSourceSongs", pyCD, pyCallback, pyOnNeedCD);
            _Unlock();
            return 0;
        }

        public bool PrepareBurning(UInt64 freeBytes)
        {
            _Lock();
            PyLong pyFreeBytes = new PyLong(freeBytes);
            PyInt pyResult = PyInt.AsInt(_py.InvokeMethod("PrepareBurning", pyFreeBytes));
            _Unlock();
            return Convert.ToBoolean(pyResult.ToInt32());
        }

        public int RenameInRespectiveLocations(ProgressCallback callback, params object[] p)
        {
            _Lock();
            PyInt pyResult = PyInt.AsInt(_py.InvokeMethod("RenameInRespectiveLocations", PyObject.FromManagedObject(callback)));
            _Unlock();
            int result = pyResult.ToInt32();
            if (result != 1)
                Board.Empty();
            return result;
        }

        #endregion
    }
}
