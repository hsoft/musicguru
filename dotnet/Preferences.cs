using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using Microsoft.VisualBasic.FileIO;

namespace musicGuru
{
    public class MainSection : ConfigurationSection
    {
        public MainSection()
        {
        }

        [ConfigurationProperty("CustomModel", DefaultValue = "%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%")]
        public string CustomModel
        {
            get { return (string)this["CustomModel"]; }
            set { this["CustomModel"] = value; }
        }

        [ConfigurationProperty("RegistrationCode", DefaultValue = "")]
        public string RegistrationCode
        {
            get { return (string)this["RegistrationCode"]; }
            set { this["RegistrationCode"] = value; }
        }

        [ConfigurationProperty("RegistrationEmail", DefaultValue = "")]
        public string RegistrationEmail
        {
            get { return (string)this["RegistrationEmail"]; }
            set { this["RegistrationEmail"] = value; }
        }

    }

    public static class Preferences
    {
        public static string CustomModel = "";
        public static string RegistrationCode = "";
        public static string RegistrationEmail = "";
        public static bool Registered = false;

        static Preferences()
        {
        }

        static public void Load()
        {
            MainSection section;
            try
            {
                Configuration conf = ConfigurationManager.OpenExeConfiguration(Path.Combine(Program.AppData, "settings"));
                section = (MainSection)conf.Sections["main"];
                if (section == null)
                    throw new Exception("Null main section, resetting to defaults");
            }
            catch
            {
                //ResetToDefault();
                //ResetColumnsToDefault();
                return;
            }
            CustomModel = section.CustomModel;
            RegistrationCode = section.RegistrationCode;
            RegistrationEmail = section.RegistrationEmail;
            Registered = HS.Reg.RegCode.IsValid(RegistrationCode, 2, RegistrationEmail);
        }

        public static void Save()
        {
            Configuration conf = ConfigurationManager.OpenExeConfiguration(ConfigurationUserLevel.None);
            MainSection section = (MainSection)conf.Sections["main"];
            if (section == null)
            {
                section = new MainSection();
                conf.Sections.Add("main", section);
            }
            section.CustomModel = CustomModel;
            section.RegistrationCode = RegistrationCode;
            section.RegistrationEmail = RegistrationEmail;
            conf.SaveAs(Path.Combine(Program.AppData, "settings.config"));
            File.Create(Path.Combine(Program.AppData, "settings")).Dispose();
        }

        public static bool AskForCode()
        {
            Registered = HS.Reg.EnterCodeDialog.AskForCode("musicGuru", 2, out RegistrationCode, out RegistrationEmail);
            return Registered;
        }
    }
}
