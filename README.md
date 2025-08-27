# P4 PYTHON PALAEO PLOTTING PROGRAM

This program allows the plotting of publication standard 'palaeo' figures for palaeo data such as testates, pollen, macrofossils, diatoms etc etc. The program produces typical plots seen in this field with taxa vs depth. The program relies on the code but also up to 3 files that the user must configure. These are the Parameter file, the Input file and potentially an Extra Input file. Input files contain the data to be plotted and some taxa specific aesthetic coding. The Parameter file contains more general aesthetic coding related to the figure and also contains the route locations of files and allows output names to be determined. 

The program was originally written in Python 3.7.6 but has been updated for 3.12.1 and uses numpy, pandas, matplotlib and argparse. 

The program was originally written by Dr Antony Blundell University of Leeds in 2022. The program has been archived in Zenodo and has an accompanying doi. 

To use the program the manual provided P4_MANUAL.pdf should be read. Without reading the manual it would be hard to understand what is a relatively simple process to create high quality plots. The manual explains the entire process from getting started with python to creating figures with example data provided from published papers or with the users own data. Examples of completed plots for the two example data sets from published work from Keighley Moor (macrofossil data) and Ardkill Moss (Testate data) are also provided as well as the input/parameter files for these. For the examples to work the user must fill in the entry in the relevant Parameter file with the folder address where they have saved the files from the repository. 

Substantial effort has been made to write as many user error checking routines as possible in this code and in most circumstances issues should be met with messages detailing the problem and provide a possible solution. 





