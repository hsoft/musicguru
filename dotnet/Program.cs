using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.IO;
using Python.Runtime;

namespace musicGuru
{
    static class Program
    {
        static private App _app;
        static public App App { get { return _app; } }
        static private string _appdata;
        static public string AppData { get { return _appdata; } }

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            string key = "hUGGQ1ER0kyqH+I57jz7CNEk4yHwLrhfQhc+CzkaHDHWAwZ3EUk3I15BvShqUdoBOTn6SMRRCVFqKYRK7LJQ+7eAKKvXogqNmIDzgE6jc+22up2VFLty6p2fyp93jnTXBs2I1fvaydcBqafgL8KA3cKhHIBgscK2TOWloBLu8LLv+rvGC73chmGrOd3XptiNWfRP2VnbAbjj3b20nvdq1ciHgaZSpwm65twghkSc4rMTrTT7p952qgC0ktQGEBo91BF5IWBL90ByCXJaBwKmCtkt8385Nahmn3AySUg3VgHed7I3Qy8OflYwN3/JJLlV9gFqep1c3VlffFwcQCaWWQple29CB7Qj+D7ebTZcw33bBjFFHDOddK4O/zisSSEN12MjSTAEMF1Pae5O7l0cQsYkHk9Kaq8atBJbSXusnYHO4rmGmPrpwXvURfvewOnqbbM4u/GG2tEn70XRBaFxiNjW26DGgUegheo636O5QvLV6L/q28Ck8WfeJs8524W3KLpKgEjgMLehhea1Nv7v8OfaEaeWhdbVo6sE//WGgN5n51ysbbBsvFvWLqe4tQbch/xOvtLRdYtBnh74JBmIbVpcry28IwAxsG0yHVZLnVpwVjxsfSxJRXViqxkWEmVEzGODUgldVRHZfYABbFwdIiQ3ukv/GdlFJSS7UcZnDVCDAGgHWm+SA9wOsDsWMmxy7B0oVeRKK1N9HYMxcnVIfj5iQ2NCLfwKZA8haiUkEDCWbwQdIDiIJmhGDFMp1j2oyJ4Mu4yYvJKckvK9YfcC6cDEvuUdw7XcUJ9Ez3OBUvmlx+rqx6e4gbP2AZzm09ihpsE8yqTqOuFhvuqKj7Nuulz2HK27uxjJqcV2wSnbieE3sx6gieMeqMqjlfZrr7mimqrBqbaCIrg3xT/NXs98mjKRqudz+CfVacjtkGJyWmdQCyB8yxSdJb5BRHS4WshUkiR3QhBJHW81e7dMdCWXXiV3kBv+WFBCyxVkMMM2NH4dIe1CsGGIDts5dAlfJtgL4h6neKV540vLO+JrzTD0d6Vps2OgZ61up22ue6tVl1GvYWYaBmkcOQRtSDI7b+hJKB3WAIkyk0KHQHgvBuuwwLK+K6Iz7mLt6eby6vPAvpqungeHGJUDmCSGzv/A4RXoCeI8ifTG3eYh13K8/8sQxjuRhYDhiYLWSp8BrveqqqlruzmrWutSqluF6PGLw9bPz6Bu+miP2IJX3uqWA+UVz0Cg6vpztqu9mswTljSkFeoQ7GmMg7uM1/vth9DDZQ5oMSHceoZtDAxuX7IGinElBydf7hD2MSVy3RAHCPQCnB3kP29opkQef3xSowH4bS44sinrZfUZ6QFzb2l5FCQVSQ==";
            StarBurn.CRegistrationClass reg = new StarBurn.CRegistrationClass();
            reg.SetLicenseKey(key);
            string appdata = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            appdata = Path.Combine(appdata, Application.CompanyName);
            appdata = Path.Combine(appdata, Application.ProductName);
            _appdata = appdata;
            PythonEngine.Initialize();
            IntPtr gil = PythonEngine.AcquireLock();
            PyObject module = PythonEngine.ImportModule("musicguru.app_dotnet");
            PyObject appClass = module.GetAttr("MusicGuru");
            _app = new App(appClass.Invoke(new PyString(_appdata)));
            PythonEngine.ReleaseLock(gil);
            Preferences.Load();
            Application.Run(new MainForm());
            Preferences.Save();
            PythonEngine.Shutdown();
        }
    }
}