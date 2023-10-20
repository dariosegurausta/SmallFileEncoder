using System.IO.Compression;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace TemplatesWithNoEndingZeros
{
    class Program
    {
        static void Main(string[] args)
        {
            var outPath = "NoZeroTemplates";
            var inPath = "OriginalTemplates";
            var zipPath = "ZipTemplates";
            var rarPath = "RarTemplates";
            try
            {
                var originalFiles = Directory.GetFiles(inPath);
                if (!Directory.Exists(outPath))Directory.CreateDirectory(outPath);
                if (!Directory.Exists(zipPath)) Directory.CreateDirectory(zipPath);
                if (!Directory.Exists(rarPath)) Directory.CreateDirectory(rarPath);
                var resultFile = new ResultFile();
                foreach(var file in originalFiles)
                {
                    var noZerosPaddingFileName = file.Replace(inPath, outPath);
                    CreateNoZeros(file, noZerosPaddingFileName);

                    var zipFile = file.Replace(inPath, zipPath).Replace(".tmp", ".zip");
                    CreateZip(noZerosPaddingFileName, zipFile);

                    var rarFile = file.Replace(inPath, rarPath).Replace(".tmp", ".rar");
                    CreateRaR(noZerosPaddingFileName, rarFile);

                    var newRowResult = new ResultRow();
                    newRowResult.FileName = file;
                    newRowResult.OriginalSize = new FileInfo(file).Length;
                    newRowResult.NoZeroPaddingFileSize = new FileInfo(noZerosPaddingFileName).Length;
                    newRowResult.ZipFileSize = new FileInfo(zipFile).Length;
                    newRowResult.RarFileSize = new FileInfo(rarFile).Length;
                    resultFile.AddRow(newRowResult);
                    Console.WriteLine(newRowResult);
                }
            }
            catch(Exception ex){
                Console.WriteLine("ERROR: "+ex.Message);
            }
        }

        static void CreateNoZeros(string Origin, string Destiny)
        {
            var datos = File.ReadAllBytes(Origin).ToList();
            while (datos[datos.Count - 1] == 0)
            {
                datos.RemoveAt(datos.Count - 1);
            }
            if (File.Exists(Destiny)) File.Delete(Destiny);
            File.WriteAllBytes(Destiny, datos.ToArray());
        }
        static void CreateZip(string Origin, string Destiny) {
            //Taken from:
            //https://stackoverflow.com/questions/2454956/create-normal-zip-file-programmatically
            using (var fileStream = new FileStream(Destiny, FileMode.Create))
            {
                using (var archive = new ZipArchive(fileStream, ZipArchiveMode.Create, true))
                {
                    var Bytes = File.ReadAllBytes(Origin);
                    var zipArchiveEntry = archive.CreateEntry(Path.GetFileName(Origin), CompressionLevel.SmallestSize);
                    using (var zipStream = zipArchiveEntry.Open())
                        zipStream.Write(Bytes, 0, Bytes.Length);
                }
            }
        }
        static void CreateRaR(string Origin, string Destity) {
            var cmd = "@echo off\r\n" +
                "\"C:\\Program Files\\WinRAR\\RAR.exe\" a " + Destity+" "+Origin+ " -idq -ep";
            System.IO.File.WriteAllText("Rar.bat",cmd);
            var process= System.Diagnostics.Process.Start("Rar.bat");
            process.WaitForExit();
        }
    }
}