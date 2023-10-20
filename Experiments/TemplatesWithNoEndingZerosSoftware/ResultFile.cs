using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.IO;
using System.Reflection.PortableExecutable;

namespace TemplatesWithNoEndingZeros
{
    internal class ResultFile
    {
        private string fileName = "Result.csv";
        private char separator= ';';
        public ResultFile() {
            var properties = (new ResultRow())
                .GetType().GetProperties().Select(p=>p.Name).ToList();
            var header= string.Join(separator,properties) ;
            File.WriteAllText(fileName,header+"\r\n");
        }
        public void AddRow(ResultRow row)
        {
            var properties = row.GetType().GetProperties().ToList();
            var valores = properties.Select(p=>
                row.GetType()
                .GetProperty(p.Name)
                .GetValue(row).ToString()
            ).ToList();
            var newRow = string.Join(separator,valores);
            File.AppendAllText(fileName,  newRow + "\r\n");
        }
    }
}
