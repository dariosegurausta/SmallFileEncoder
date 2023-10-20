using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TemplatesWithNoEndingZeros
{
    internal class ResultRow
    {
        public string FileName { get; set; }
        public long  OriginalSize { get; set; }
        public long  NoZeroPaddingFileSize { get; set; }
        public long ZipFileSize { get; set; }
        public long RarFileSize { get; set; }
        public override string ToString()
        {
            var properties = this.GetType().GetProperties().ToList();
            var valores = properties.Select(p =>
                this.GetType()
                .GetProperty(p.Name)
                .GetValue(this).ToString()
            ).ToList();
            var row = string.Join(" ", valores);
            return row;
        }
    }
}
