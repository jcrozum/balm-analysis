`mtsNFVS` is a Python package for computing complex attractors in asynchronous Boolean networks.
Author: Van-Giang Trinh, Belaid Benhamou, Tarek Khaled, and Kunihiko Hiraishi
Contact: Van-Giang Trinh (giang.trinh91@gmail.com)

# Requirements:
- Operating system: Linux
- JRE version 1.8 or higher
- GCC version 7.3.0 or higher
- Clingo (<https://sourceforge.net/projects/potassco/files/clingo/>)

# Run `mtsNFVS` from the command line

``` sh
$ python test.py file_name.bnet
```

# Notes

+ The model file must be a file with extension `.bnet` with the BoolNet format (<http://colomoto.org/biolqm/doc/format-bnet.html>).
+ The model file must be placed in the `networks` folder.
+ The `predata` folder contains the `file_name.mts` file storing the set of minimal trap spaces, the `file_name.std` file storing the set of fixed points of the reduced STG, and the `file_name.an` file that is converted from the `file_name.bnet` file by using bioLQM.jar.
+ Please don't delete the `temp`, `external`, `predata` folders.



