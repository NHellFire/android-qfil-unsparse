# android-qfil-unsparse
Tool to reassemble the sparse images used by Qualcomm Flash Image Loader

```
usage: qfil-unsparse [-h] [-x XML] [-p PARTITION | -l] [-o DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -x XML, --xml XML     XML file to parse for partitions (default:
                        rawprogram0.xml)
  -p PARTITION, --partition PARTITION
                        Partition to assemble (default: all)
  -l, --list            List found partitions
  -o DIRECTORY, --output DIRECTORY
                        Output directory (default: Current directory)
```

Running `qfil-unsparse` with no arguments will extract all sparse partitions from the firmware described in `rawprogram0.xml` located in the current directory.


This has been tested working on the Lenovo Tab4 8 Plus firmware.

If you've got another firmware using QFIL that this tool can't reassemble, open an issue providing a download link.


---



### Installation


You can either:

&nbsp;&nbsp;&nbsp;&nbsp;a. Clone this repo  
&nbsp;&nbsp;&nbsp;&nbsp;b. Install using pip: `pip install git+https://github.com/NHellFire/android-qfil-unsparse.git`

