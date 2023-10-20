****************************************************************************************************
This forder contains the software for compress the original fingerprints templates and the results.
****************************************************************************************************
1. TemplatesWithNoEndingZerosSoftware: contains C# console application project, this application reads the original fingerprints templates remove ending zeros and store this information in a nes file. Then, compress this file using ZIP and RAR tools and store the results, for each fingerprint template file. Finally, store into CSV file information about file name and sizes files for each template processed.
2. TemplateWithNoEndingZerosResults: shows the result files after experiments. There are four folders:
   2.1. OriginalTemplates: contains files with original fingerprint template delivered by the fingerprint sensor FPM10A.
   2.2. NoZeroTemplates: contains files with fingerprint template without ending zeros padding.
   2.3. ZipTemplates: contains the files with the NoZeroEndings codded with ZIP tools.
   2.4. RarTemplates: contains the files with the NoZeroEndings codded with RAR tools.
