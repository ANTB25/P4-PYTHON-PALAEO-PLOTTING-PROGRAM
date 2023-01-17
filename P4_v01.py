# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:32:47 2022

@author: A.Blundell
"""
###############################################################################
# P4 PALAEO PLOTTING PROGRAM written by Dr Antony Blundell 
# School of Geography, University of Leeds, 2022

# Program is used to plot palaeo data such as pollen, testate amoebae, diatoms,
# macrofossils etc in a depth vs abundance way. The program is intended to 
# produce high quality plots quickly that are good enough for publication. The
# program is for plotting only and has no statistical element. There is the 
# option for two Stack plots at present to make percentages of 
# specified groups of taxa. Please see the manual.

# The program relies on the code below but also two/three csv files. One 
# containing the raw data to be plotted (input file) and some taxon related 
# aethetics and a second where general parameters (parameter file) of the 
# plots are defined and can be altered. The parameter file location and file 
# name is nominated on the cmd line when running the program and is the route 
# of all the other information required by the program. A third csv file 
# nominally called the extra file here (name can be altered in parameters.csv 
# file) contains input data like the input file but has data you wish to use 
# as a multiple entry on a single plot. So for example three lines on the same
# plot like might be carried out for testate wt reconstructions with plus and 
# minus errors (see manual for explanation).

# Data to be plotted (input file) and the output is kept / sent to the 
# directory nominated by the user as part of the parameter file.

# Plots are produced in portrait. Once produced plots can easily be rotated to
# landscape from file explorer. To aid faster production whilst getting the 
# plot looking as required it is best to keep the specified dpi low (150 for 
# example) in the parameter file so that the process is fast. Once happy the 
# user can ramp up the dpi to get a much higher resolution product. The time
# for each iteration of rebuilding the figure depends on the amount of data 
# but as an example the example plots in the manual take about 20 seconds from
# program run to product in the designated location at at 800 dpi. Output can 
# be png, pdf or svg and that can be specified in the parameter file.

# Particularly fancy additions to the plots are best carried out in a drawing
# package after the main body of the plot is constructed here. However, zones
# and rc date additions, date lines and grouping annotations can be added here
# and most aspects of the plot can be altered. Grouping annotations are 
# possible but this is a little fiddly but once practiced is simple enough.
# Very specific things can easily be added in external programs such as 
# Inkscape. Exaggeration of plots is possible and differing levels of 
# exaggeration can be specified for the taxa. This is only possible on set 
# plot types and the exaggeration plot will either be a line or a filled area
# plot.

# Code is run from the command line and the parameter file location and name 
# is provided as part of the command when running the program . See manual for
# how to do this.

# The program has been developed while using microsoft windows 10. However, 
# the code runs in mac or linux (see manual for instructions).

###############################################################################
#### This program was written by Dr Antony Blundell, School of Geography, #####
################# University of Leeds, Leeds in 2022. #########################
###############################################################################

###############################################################################
################# Please cite the doi reference if you use ####################
################### this to create plots in publications. #####################
###############################################################################

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, \
                   AutoMinorLocator)
from matplotlib.gridspec import GridSpec
from matplotlib.patches import ConnectionPatch
import matplotlib
import sys
from pathlib import Path
import argparse

###############################################################################
###############################################################################
# Create argument for command line so initial location for parameter file and
# its name can be stated.
parser = argparse.ArgumentParser(description = \
                           "Variables for file and location" )
parser.add_argument('--input', action ='store', type = str, nargs = 2)

args = parser.parse_args()

location = args.input[0]
file_name = args.input[1]

# If using from an IDE comment out argparse part above and use the two lines
# below. Fill them in with parameter file location separarted by \\. Fill in 
# the parameter file name.
# location = "C:\\Users"
# file_name = "KM_Macro_Parameter_LOI.csv"

###############################################################################
###############################################################################
def main ():
    # Print out Program title, author and place of origin
    print("")
    print("P4 ")
    print("(PYTHON PALAEO PLOTTING PROGRAM) written by Dr Antony Blundell")
    print("School of Geography, University of Leeds, 2022")
    
    # The program uses a user preferences form the Parameter file, the location
    # of which is supplied in the information above from the cmd line.
    try:
        os.chdir(location)
    except:
        print("\nProblem with address of Parameter file. Is it spelt "
              "correctly, in the correct location or actually exist?")
        sys.exit()
    
    # The Parameter file holds information related to the parameters used
    # to construct the plot. This does not include the raw data of the 
    # palaeo-record being plotted which is held in the Input file. The name 
    # and location of which is stated in the Parameter file. 
    
    # Check file provided is a csv file and that it exists.
    if ".csv" in file_name:
        try:
            par = pd.read_csv(file_name)
        except:
            print("\nProblem with the Parameter file name. Is it spelt "
                  "correctly, in correct location or exist at all?")
            sys.exit()
    else:
        print("\nParameter file required in comma delimited csv format.")
        sys.exit()
    
    # Print Gathering Paremeters to signify to user the program is commencing
    print("") 
    print("\n **Gathering Parameters**")
    print("")
    
    # Create lists of items from the columns in the Parameter file including the
    # users entries and the Title of the parameter itself
    par_list_0 = [x for x in par["PARAMETERS"][0::]]
    par_list_1 = [x for x in par["ENTRY"][0::]]
    
    # Create dictionary of parameter entries and associated values/text.
    par_dict = {Q: R for Q, R in zip(par_list_0, par_list_1)}
    
    # Initial error checking of essential entries from Parameter file. If any 
    # of these are blank then the program will stop. 
    # Create lists of values from Parameter file that are essential entries  
    # ready for checking.
    par_list_G1_values = par_list_1[4:9]
    par_list_G2_values = par_list_1[15:17]
    par_list_G3_values = par_list_1[21:22]
    par_list_G4_values = par_list_1[28:29]
    par_list_G5_values = par_list_1[42:43]
    par_list_G6_values = par_list_1[54:59]
    par_list_G7_values = par_list_1[64:67] + par_list_1[68:71] + \
                         par_list_1[72:73] + par_list_1[74:77]
    par_list_G8_values = par_list_1[82:84]
    par_list_G9_values = par_list_1[89:90] + par_list_1[91:94] + \
                         par_list_1[95:96] + par_list_1[97:101]
    par_list_G10_value = par_list_1[106:107]
    par_list_G11_value = par_list_1[138:139]
    par_list_G12_value = par_list_1[159:160]
    par_list_G13_values = par_list_1[187:188] + par_list_1[204:205] + \
                         par_list_1[221:222] + par_list_1[238:239] + \
                         par_list_1[255:256] + par_list_1[272:273] + \
                         par_list_1[289:290] + par_list_1[306:307] + \
                         par_list_1[323:324] + par_list_1[340:341]
    par_list_G14_values = par_list_1[361:366]
    
    # Initial general error checking of user preferences in Parameter file.
    for x in par_list_G1_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 1 "
                  "is/are missing.")
            sys.exit()
    
    for x in par_list_G2_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 2 "
                  "is/are missing.") 
            sys.exit()
        
    for x in par_list_G3_values:
        if isinstance(x, str) == False:
            print("\nEssential entry in Parameter file, Group 3 is incorrect."
                  " Check entry and format.")
            sys.exit()
        if pd.isnull(x) == True:
            print("\nEssential entry in Parameter file, Group 3 is missing.") 
            sys.exit()
        
    for x in par_list_G4_values:
        if pd.isnull(x) == True:
            print("\nEssential entry for Overall title on/off in Parameter "
                  "file is missing. Enter 'on' or 'off'.") 
            sys.exit()
            
    for x in par_list_G5_values:
        if pd.isnull(x) == True:
            print("\nEssential entry for Footer text on/off in Parameter file"
                  " is missing.") 
            sys.exit()     
            
    for x in par_list_G6_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 6 "
                  "is/are missing.")
            sys.exit()
        
    for x in par_list_G7_values:
        if pd.isnull(x) == True:
            print("\nEssential entries / entry in Parameter file, Group 7 "
                  "is/are missing.") 
            sys.exit()
        
    for x in par_list_G8_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 8 "
                  "is/are missing.") 
            sys.exit()
            
    for x in par_list_G9_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 9 "
                  "is/are missing.")
            sys.exit()
    
    if pd.isnull(par_list_G10_value) == True:
        print("\nZones on/off entry in Parameter file, Group 10 is missing.") 
        sys.exit()
        
    if pd.isnull(par_list_G11_value) == True:
        print("\nRC ages on/off entry in Parameter file, Group 11 is missing.")
        sys.exit()
            
    if pd.isnull(par_list_G12_value) == True:
        print("\nINT ages on/off entry in Parameter file Group 12 is missing.")
        sys.exit()
        
    for x in par_list_G13_values:
        if pd.isnull(x) == True:
            print("\nEssential entries/entry in Parameter file, Group 13 "
                  "is/are missing.")         
            sys.exit()   
            
    for x in par_list_G14_values:
        if pd.isnull(x) == True:
            print("\nIf any NSC not being used add 'none' to the relevent NSC "
                  "1 - 5 entry in Parameter file, Group 14.") 
            sys.exit() 
            
    # Colours are from 1-23. This can be added to by the user if 
    # required (look up matplotlib colours). Just add more to the colour 
    # function and change the maximum colour number here. Declare number here
    # as checks  require this value.
    col_max = 23 
    
    ###########################################################################
    ###########################################################################
    # Change working directory stated in Parameter file and load in raw data
    # to be plotted from Input file. 
    os.chdir(par_dict["Directory**"]) 
    input_filename = par_dict["Input file name**"]
    
    # Error checking for Input file import
    try:
        data = pd.read_csv(par_dict["Input file name**"])
    except:
        print(f"\nProblem loading in Input file. Is {input_filename} the "
              "correct name and in correct location ? Check location and "
              "spelling of name.")
        sys.exit()
    
    # Look for blanks in the Input file. If there are blanks give message and 
    # exit the program. Entries if not required should be filled with values of
    # zero
    for name, values in data.iteritems():
        for x in values:
            if pd.isnull(x) == True:
                print(f"\nEntry missing in input file in the {name} column."
                      " There should be no blank entries. If it is a numeric "
                      "value use a zero.")
                sys.exit()
        
    # Load in Extra Input file if required. File with information for plots  
    # with multiple entries.
    extra_yn = str(par_dict["Extra input file name**"]).strip()
    extra_input_filename = str(par_dict["Extra input file name**"])
    
    # Error check importing of Extra Input file if user needs to use it
    if extra_yn != "none":
        try:
            data_extra = pd.read_csv(par_dict["Extra input file name**"])
        except:
            print(f"\nProblem loading in Extra Input file. Is "
                  f"{extra_input_filename} the correct name and in correct "
                  "location ? Check location and spelling of name.")
            sys.exit()
            
    # Remove columns in dataframes if have no values other than zero. Palaeo 
    # data should not have sums of zero or no data for any taxa. Pointless 
    # being there.If any are then the program removes the column automatically
    # for use in the  program.
    for name, values in data.iloc[38::,2:].iteritems():
        if values.sum() == 0:
            data.drop(name, axis = 1, inplace = True)
            
        # Check input data for non numeric values
        for x in values:
            if np.isreal(x) == False:
                print(f"\nThere is a non numeric element in the {name} "
                      "column in the data frame. Data needs to be numeric.")
                sys.exit()
            
    # As above but for Extra Input file
    if extra_yn != "none":
    
    # Look for blanks in the Extra Input file if used. If there are blanks give
    # message and exit the program.
        for name, values in data_extra.iteritems():
            for x in values:
                if pd.isnull(x) == True:
                    print(f"\nEntry missing in Extra input file in the {name}"
                          " column.There should be no blank entries. If it is"
                          " a numeric value use a zero.")
                    sys.exit()
        
        for name, values in data_extra.iloc[38::,2:].iteritems():
            if values.sum() == 0:
                data_extra.drop(name, axis = 1, inplace = True)
    
    # Determine stated output file name for pdf, png and svg outputs from 
    # Parameters.csv file.
    output_name = par_dict["Output file name**"]
    
    ###########################################################################
    ###########################################################################
    # Determine if Zones are required or not as specified by user.
    zones_on_off = par_dict["Zones on/off**"].replace(" ","").lower()
    
    # Obtain list of titles of taxa to be plotted from the Input files
    # (standard and extra).
    data_list = [col for col in data.columns]
    
    # The first column must be called Depth and be the data used the x axis 
    # (portrait) and always be the first column once the data file has been 
    # trimmed. The last column whether Zones are required or not should always
    # be called Zones. If not create an error message.
    if data_list [1] != "Depth" or data_list [-1] != "Zones":
        print("\nThe second and last column of the input file must be the "
              "'Depth' and 'Zones' columns. One or both are incorrect. Make "
              "sure there are no spaces before or after the word 'Depth' or "
              "'Zones' See manual for correct setup.")
        sys.exit()
    
    # Make list of all Palaeo data names (not including Depth) but including
    # Zones as Zones plots as their own column on plot like a taxa. Reverse 
    # the list.
    data_list = data_list[2:]
    data_list = data_list[::-1]
    
    # Create taxa lists for Extra Input file if required by user. Check that
    # is set up correctly like above with Depth and Zones columns at either
    # end and reverse list 
    if extra_yn != "none":
        data_list_extra = [col for col in data_extra.columns]
        
        if data_list_extra [1] != "Depth" or data_list_extra [-1] != "Zones":
            print("\nThe second and last column of the extra input file must "
                  "be the 'Depth' and 'Zones' columns. One or both are "
                  "incorrect. Make sure there are no spaces before or after "
                  "the word 'Depth' or 'Zones' See manual for correct setup.")
            sys.exit()
        
        data_list_extra = data_list_extra[2:]
        data_list_extra = data_list_extra[::-1]   
    
    # If zones are not requested in Parameter file remove the Zones title 
    # from the list of taxa
    if zones_on_off == "off":
        data_list = data_list[1::]
    
    # Data_list_1 is the first taxon and has depth plotted with it with labels 
    # etc. Data_list_1 is used to identify this later in code for plotting for 
    # main dataframe only not extra.
    data_list_1 = data_list[-1]
    
    # Create dataframe of taxa and graph type choices selecetd by user from 
    # Input file and remove Depth which always has zero value as is meaningless
    data_1 = data.iloc[0:1,1::].transpose()
    data_1 = data_1.drop("Depth")
    
    # If zones not requested by user remove from dataframe of taxa and graph 
    # type choices 
    if zones_on_off == "off":
        data_1 = data_1.drop("Zones")
    
    # Change dataframe titles to Taxa and graph and sort alphabetically   
    data_1 = data_1.reset_index()
    data_1.rename(columns = {"index": "TAXA"}, inplace = True)
    data_1.rename(columns = {0: "graph"}, inplace = True)
    data_1 = data_1.sort_values("TAXA")
    
    # Create dictionary of taxa to be plotted and associated 'plot style' 
    # reference numbers, plot style numbers are from 1-7.
    # 1 is a barplot 
    # 2 is a bar and lineplot,
    # 3 lineplot 
    # 4 is a lineplot with shaded section under the line
    # 5 is a line and marker plot,
    # 6 is a marker plot only
    # 7 is a stack plot (only 2 of these are possible at present).
    # Plot style 1-7 is listed in row 2 of the input file by user.
    taxa, plot = list(data_1.iloc[:,0]), list(data_1.iloc[:,1])
    plot_type = {taxons: plot_styles for taxons, plot_styles \
                 in zip(taxa, plot)}
    
    # Error checking for plot type number 7. Only two instances of this plot
    # type are allowed at present. Can incresae with additional code.
    if sum(value == 7 for value in plot_type.values()) > 2:
        print("\nOnly 2 stack style plots are available at present. More "
              "than 2 have been specified.")
        sys.exit()
         
    # For 'extra' data obtain taxon names.
    if extra_yn != "none":
        taxa_extra = data_list_extra
    
    # Create list of taxa to be plotted and the order number they are in the
    # data provided (this is reversed)
    data_list_dict = {k: v for k, v in zip(data_list, \
                                           np.arange(0, len(data_list), 1))}
    
    ###########################################################################
    ###########################################################################
    # Get user options from the Input file
    
    ###########################################################################
    # Get colour index values for bars for graph types 1, 2 from Input file.
    # These are 1-23 (see manual). More colours can be added if required.
    bar_col = data.iloc[1:2,1::].transpose()
    bar_col = bar_col.drop("Depth")
    
    if zones_on_off == "off":
        bar_col = bar_col.drop("Zones")
       
    bar_col = bar_col.reset_index()
    bar_col.rename(columns = {"index": "TAXA"}, inplace = True)
    bar_col.rename(columns = {1: "bar_colour"}, inplace = True)
    bar_col = bar_col.sort_values ("TAXA")
    
    # Create dictionary of taxa titles and plot colour indexes.
    taxa_bar_col, bar_colour = list(bar_col.iloc [:,0]), list(bar_col.iloc \
                                                              [:,1])
    bar_col_type = {taxa_bar_cols: colours for taxa_bar_cols, colours \
                    in zip(taxa_bar_col, bar_colour)}
    
    ###########################################################################
    # Get width values for bars for graph type 1 from Input file (see manual).
    bar_w_g1 = data.iloc[2:3,1::].transpose()
    bar_w_g1 = bar_w_g1.drop("Depth")
    
    if zones_on_off == "off":
        bar_w_g1 = bar_w_g1.drop("Zones")
        
    bar_w_g1 = bar_w_g1.reset_index()
    bar_w_g1.rename(columns = {"index": "TAXA"}, inplace = True)
    bar_w_g1.rename(columns = {1: "WIDTH"}, inplace = True)
    bar_w_g1 = bar_w_g1.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_bar_g1_width, bar_g1_width = list(bar_w_g1.iloc [:,0]), \
                                      list(bar_w_g1.iloc [:,1])
    bar_wid_g1 = {taxa_bar_g1_widths: bar_g1_widths for taxa_bar_g1_widths, \
                  bar_g1_widths in zip(taxa_bar_g1_width, bar_g1_width)}
    
    ###########################################################################
    # Get width values for bars for graph type 2 from Input file (see manual).
    bar_w = data.iloc[3:4,1::].transpose()
    bar_w = bar_w.drop("Depth")
    
    if zones_on_off == "off":
        bar_w = bar_w.drop("Zones")
        
    bar_w = bar_w.reset_index()
    bar_w.rename(columns = {"index": "TAXA"}, inplace = True)
    bar_w.rename(columns = {1: "WIDTH"}, inplace = True)
    bar_w = bar_w.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_bar_width, bar_width =list(bar_w.iloc [:,0]), list(bar_w.iloc [:,1])
    bar_wid = {taxa_bar_widths: bar_widths for taxa_bar_widths, bar_widths \
               in zip(taxa_bar_width, bar_width)}
    
    ###########################################################################
    # Get linestyle values for lines for graphs 2, 3, 4, and 5 from 
    # Input files (see manual).
    line_s = data.iloc[4:5,1::].transpose()
    line_s = line_s.drop("Depth")
    
    if zones_on_off == "off":
        line_s = line_s.drop("Zones")
        
    line_s = line_s.reset_index()
    line_s.rename(columns = {"index": "TAXA"}, inplace = True)
    line_s.rename(columns = {1: "style"}, inplace = True)
    line_s = line_s.sort_values ("TAXA")
    
    # Create dictionary of above.
    taxa_line_style, line_style = list(line_s.iloc [:,0]), \
                                  list(line_s.iloc [:,1])
                                  
    line_type = {taxa_line_styles: line_styles for taxa_line_styles, \
                 line_styles in zip(taxa_line_style, line_style)}
    
    # As above for extra data file if required by user
    if extra_yn != "none":
        line_s_ex = data_extra.iloc[4:5,1::].transpose()
        line_s_ex = line_s_ex.drop("Depth")
        
        if zones_on_off == "off":
            line_s_ex = line_s_ex.drop("Zones")
            
        line_s_ex = line_s_ex.reset_index()
        line_s_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        line_s_ex.rename(columns = {1: "style"}, inplace = True)
        line_s_ex = line_s_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_line_style_ex, line_style_ex = list(line_s_ex.iloc[:,0]), \
                                            list(line_s_ex.iloc[:,1])
        line_type_ex = {taxa_line_style_exs: line_style_exs for \
                        taxa_line_style_exs, line_style_exs in \
                            zip(taxa_line_style_ex, line_style_ex)}
    
    ###########################################################################
    # Get line colour values for lines for graphs 2, 3, 4, and 5 from Input
    # files (see manual).
    line_col = data.iloc[5:6,1::].transpose()
    line_col = line_col.drop("Depth")
    
    if zones_on_off == "off":
        line_col = line_col.drop("Zones")
        
    line_col = line_col.reset_index()
    line_col.rename(columns = {"index": "TAXA"}, inplace = True)
    line_col.rename(columns = {1: "colour"}, inplace = True)
    line_col = line_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_line_col, line_colour = list(line_col.iloc[:,0]), \
                                 list(line_col.iloc[:,1])
    line_colour_type = {taxa_line_cols: line_colours for taxa_line_cols, \
                        line_colours in zip(taxa_line_col, line_colour)}
    
    # As above for extra data file if required by user
    if extra_yn != "none":
        line_col_ex = data_extra.iloc[5:6,1::].transpose()
        line_col_ex = line_col_ex.drop("Depth")
        
        if zones_on_off == "off":
            line_col_ex = line_col_ex.drop("Zones")
            
        line_col_ex = line_col_ex.reset_index()
        line_col_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        line_col_ex.rename(columns = {1: "colour"}, inplace = True)
        line_col_ex = line_col_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_line_col_ex, line_colour_ex = list(line_col_ex.iloc[:,0]), \
                                           list(line_col_ex.iloc[:,1])
        line_colour_type_ex= {taxa_line_col_exs: line_colour_exs for \
                              taxa_line_col_exs, line_colour_exs \
                              in zip(taxa_line_col_ex, line_colour_ex)}
    
    ###########################################################################
    # Get fill colour values for graphs 2 and 4 from Input files (see manual).
    fill_col= data.iloc[6:7,1::].transpose()
    fill_col= fill_col.drop("Depth")
    
    if zones_on_off == "off":
        fill_col= fill_col.drop("Zones")
        
    fill_col= fill_col.reset_index()
    fill_col.rename(columns = {"index": "TAXA"}, inplace = True)
    fill_col.rename(columns = {1: "colour"}, inplace = True)
    fill_col= fill_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_fill_col, fill_colour = list(fill_col.iloc[:,0]), \
                                 list(fill_col.iloc[:,1])
    fill_colour_type = {taxa_fill_cols: fill_colours for taxa_fill_cols, \
                        fill_colours in zip(taxa_fill_col, fill_colour)}
    
    ###########################################################################
    # Get fill colour transparency values for graphs 2 and 4 from Input files 
    # (see manual).
    fill_t = data.iloc[7:8,1::].transpose()
    fill_t = fill_t.drop("Depth")
    
    if zones_on_off == "off":
        fill_t= fill_t.drop("Zones")
        
    fill_t= fill_t.reset_index()
    fill_t.rename(columns = {"index": "TAXA"}, inplace = True)
    fill_t.rename(columns = {1: "TRANS"}, inplace = True)
    fill_t= fill_t.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_fill_tran, fill_tran = list(fill_t.iloc[:,0]), \
                                list(fill_t.iloc[:,1])
    fill_trans_type = {taxa_fill_trans: fill_trans for taxa_fill_trans, \
                       fill_trans in zip(taxa_fill_tran, fill_tran)}
    
    ###########################################################################
    # Get line width values for graphs 2, 3, 4, 5 and 7 from Input files (see 
    # manual).
    line_wid = data.iloc[8:9,1::].transpose()
    line_wid = line_wid.drop("Depth")
    
    if zones_on_off == "off":
        line_wid = line_wid.drop("Zones")
        
    line_wid = line_wid.reset_index()
    line_wid.rename(columns = {"index": "TAXA"}, inplace = True)
    line_wid.rename(columns = {1: "WIDTH"}, inplace = True)
    line_wid = line_wid.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_line_width, line_width = list(line_wid.iloc[:,0]), \
                                  list(line_wid.iloc[:,1])
    line_width_type = {taxa_line_widths: line_widths for taxa_line_widths, \
                       line_widths in zip(taxa_line_width, line_width)}
    
    # As above for extra data file if requested by user
    if extra_yn != "none":
        line_wid_ex = data_extra.iloc[8:9,1::].transpose()
        line_wid_ex = line_wid_ex.drop("Depth")
        
        if zones_on_off == "off":
            line_wid_ex = line_wid_ex.drop("Zones")
            
        line_wid_ex = line_wid_ex.reset_index()
        line_wid_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        line_wid_ex.rename(columns = {1: "WIDTH"}, inplace = True)
        line_wid_ex = line_wid_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_line_width_ex, line_width_ex = list(line_wid_ex.iloc[:,0]), \
                                            list(line_wid_ex.iloc[:,1])
        line_width_type_ex = {taxa_line_width_exs:line_width_exs for \
                              taxa_line_width_exs, line_width_exs\
                               in zip(taxa_line_width_ex, line_width_ex)}
    
    ###########################################################################
    # Get marker type values for graphs 5 and 6 from Input files (see manual).
    marker_typ = data.iloc[9:10,1::].transpose()
    marker_typ = marker_typ.drop("Depth")
    
    if zones_on_off == "off":
        marker_typ = marker_typ.drop("Zones")
        
    marker_typ = marker_typ.reset_index()
    marker_typ.rename(columns = {"index": "TAXA"}, inplace = True)
    marker_typ.rename(columns = {1: "TYPE"}, inplace = True)
    marker_typ = marker_typ.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_marker_type, marker_type = list(marker_typ.iloc[:,0]), \
                                    list(marker_typ.iloc[:,1])
    marker_typ_type = {taxa_marker_types: marker_types for taxa_marker_types, \
                       marker_types in zip(taxa_marker_type, marker_type)}
    
    # As above for extra data file if requested by user
    if extra_yn != "none":
        marker_typ_ex = data_extra.iloc[9:10,1::].transpose()
        marker_typ_ex = marker_typ_ex.drop("Depth")
        
        if zones_on_off == "off":
            marker_typ_ex = marker_typ_ex.drop("Zones")
            
        marker_typ_ex = marker_typ_ex.reset_index()
        marker_typ_ex.rename(columns = {"index":"TAXA"}, inplace = True)
        marker_typ_ex.rename(columns = {1: "TYPE"}, inplace = True)
        marker_typ_ex = marker_typ_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_marker_type_ex, marker_type_ex = list(marker_typ_ex.iloc[:,0]), \
                                              list(marker_typ_ex.iloc[:,1])
        marker_typ_type_ex = {taxa_marker_type_exs: marker_type_exs for \
                              taxa_marker_type_exs, marker_type_exs \
                              in zip(taxa_marker_type_ex, marker_type_ex)}
    
    ###########################################################################
    # Get marker size values for graphs 5 and 6 from Input files (see manual).
    marker_s = data.iloc[10:11,1::].transpose()
    marker_s = marker_s.drop("Depth")
    
    if zones_on_off == "off":
        marker_s = marker_s.drop("Zones")
        
    marker_s = marker_s.reset_index()
    marker_s.rename(columns = {"index": "TAXA"}, inplace = True)
    marker_s.rename(columns = {1: "SIZE"}, inplace = True)
    marker_s = marker_s.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_marker_size, marker_size = list(marker_s.iloc[:,0]), \
                                    list(marker_s.iloc[:,1])
    marker_s_size = {taxa_marker_sizes: marker_sizes for taxa_marker_sizes, \
                     marker_sizes in zip(taxa_marker_size, marker_size)}
    
    # As above for extra data file if requested by user
    if extra_yn != "none":
        marker_s_ex = data_extra.iloc[10:11,1::].transpose()
        marker_s_ex = marker_s_ex.drop("Depth")
        
        if zones_on_off == "off":
            marker_s_ex = marker_s_ex.drop("Zones")
            
        marker_s_ex = marker_s_ex.reset_index()
        marker_s_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        marker_s_ex.rename(columns = {1: "SIZE"}, inplace = True)
        marker_s_ex = marker_s_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_marker_size_ex, marker_size_ex = list(marker_s_ex.iloc[:,0]), \
                                              list(marker_s_ex.iloc[:,1])
        marker_s_size_ex = {taxa_marker_size_exs: marker_size_exs \
                            for taxa_marker_size_exs, \
                            marker_size_exs in zip(taxa_marker_size_ex, \
                            marker_size_ex)}
    
    ###########################################################################
    # Get marker face colour values for graphs 5 and 6 from Input files (see 
    # manual).
    marker_f = data.iloc[11:12,1::].transpose()
    marker_f = marker_f.drop("Depth")
    
    if zones_on_off == "off":
        marker_f = marker_f.drop("Zones")
        
    marker_f = marker_f.reset_index()
    marker_f.rename(columns = {"index": "TAXA"}, inplace = True)
    marker_f.rename(columns = {1: "colour"}, inplace = True)
    marker_f = marker_f.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_marker_f_col, marker_f_col = list(marker_f.iloc[:,0]), \
                                      list(marker_f.iloc[:,1])
    marker_f_col = {taxa_marker_f_cols: marker_f_cols for taxa_marker_f_cols, \
                    marker_f_cols in zip(taxa_marker_f_col, marker_f_col)}
    
    # As above for extra data file if requested by user
    if extra_yn != "none":
        marker_f_ex = data_extra.iloc[11:12,1::].transpose()
        marker_f_ex = marker_f_ex.drop("Depth")
        
        if zones_on_off == "off":
            marker_f_ex = marker_f_ex.drop("Zones")
            
        marker_f_ex = marker_f_ex.reset_index()
        marker_f_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        marker_f_ex.rename(columns = {1: "colour"}, inplace = True)
        marker_f_ex = marker_f_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_marker_f_col_ex, marker_f_col_ex = list(marker_f_ex.iloc[:,0]), \
                                                list(marker_f_ex.iloc[:,1])
        marker_f_col_ex = {taxa_marker_f_col_exs: marker_f_col_exs \
                           for taxa_marker_f_col_exs, marker_f_col_exs \
                               in zip(taxa_marker_f_col_ex, marker_f_col_ex)}
    
    ###########################################################################
    # Get marker edge colour values for graphs 5 and 6 from Input files (see 
    # manual).
    marker_e = data.iloc[12:13,1::].transpose()
    marker_e = marker_e.drop("Depth")
    
    if zones_on_off == "off":
        marker_e= marker_e.drop("Zones")
        
    marker_e = marker_e.reset_index()
    marker_e.rename(columns = {"index": "TAXA"}, inplace = True)
    marker_e.rename(columns = {1: "colour"}, inplace = True)
    marker_e = marker_e.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_marker_e_col, marker_e_col = list(marker_e.iloc[:,0]), \
                                      list(marker_e.iloc[:,1])
    marker_e_col = {taxa_marker_e_cols: marker_e_cols for taxa_marker_e_cols, \
                    marker_e_cols in zip(taxa_marker_e_col, marker_e_col)}
    
    # As above for extra data file if requested by user.
    if extra_yn != "none":
        marker_e_ex = data_extra.iloc[12:13,1::].transpose()
        marker_e_ex = marker_e_ex.drop("Depth")
        
        if zones_on_off == "off":
            marker_e_ex = marker_e_ex.drop("Zones")
            
        marker_e_ex = marker_e_ex.reset_index()
        marker_e_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        marker_e_ex.rename(columns = {1: "colour"}, inplace = True)
        marker_e_ex = marker_e_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_marker_e_col_ex, marker_e_col_ex = list(marker_e_ex.iloc[:,0]), \
                                                list(marker_e_ex.iloc[:,1])
        marker_e_col_ex = {taxa_marker_e_col_exs: marker_e_col_exs for \
                           taxa_marker_e_col_exs, marker_e_col_exs \
                           in zip(taxa_marker_e_col_ex, marker_e_col_ex)}
    
    ###########################################################################
    # Get marker edge width values for graphs 5 and 6 from Input files (see 
    # manual).
    marker_e_w = data.iloc[13:14,1::].transpose()
    marker_e_w = marker_e_w.drop("Depth")
    
    if zones_on_off == "off":
        marker_e_w = marker_e_w.drop("Zones")
        
    marker_e_w = marker_e_w.reset_index()
    marker_e_w.rename(columns = {"index": "TAXA"}, inplace = True)
    marker_e_w.rename(columns = {1: "WIDTH"}, inplace = True)
    marker_e_w = marker_e_w.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_marker_e_w_wid, marker_e_w_wid = list(marker_e_w.iloc[:,0]), \
                                          list(marker_e_w.iloc[:,1])
    marker_e_w_wid = {taxa_marker_e_w_wids: marker_e_w_wids for \
                      taxa_marker_e_w_wids, marker_e_w_wids \
                      in zip(taxa_marker_e_w_wid, marker_e_w_wid)}
    
    # As above for extra data file if requested by user.
    if extra_yn != "none":
        marker_e_w_ex = data_extra.iloc[13:14,1::].transpose()
        marker_e_w_ex = marker_e_w_ex.drop("Depth")
        
        if zones_on_off == "off":
            marker_e_w_ex = marker_e_w_ex.drop("Zones")
            
        marker_e_w_ex = marker_e_w_ex.reset_index()
        marker_e_w_ex.rename(columns = {"index": "TAXA"}, inplace = True)
        marker_e_w_ex.rename(columns = {1: "WIDTH"}, inplace = True)
        marker_e_w_ex = marker_e_w_ex.sort_values("TAXA")
        
        # Create dictionary of above.
        taxa_marker_e_w_wid_ex, marker_e_w_wid_ex \
                                = list(marker_e_w_ex.iloc[:,0]), \
                                  list(marker_e_w_ex.iloc[:,1])
        marker_e_w_wid_ex = {taxa_marker_e_w_wid_exs: marker_e_w_wid_exs \
                             for taxa_marker_e_w_wid_exs, marker_e_w_wid_exs \
                             in zip(taxa_marker_e_w_wid_ex, \
                             marker_e_w_wid_ex)}
    
    ###########################################################################
    # Obtain colour value for taxon title colour from 1-23 (see manual) from
    # Input files.
    taxon_c = data.iloc[14:15,1::].transpose()
    taxon_c = taxon_c.drop("Depth")
    
    if zones_on_off == "off":
        taxon_c = taxon_c.drop("Zones")
        
    taxon_c = taxon_c.reset_index()
    taxon_c.rename(columns = {"index": "TAXA"}, inplace = True)
    taxon_c.rename(columns = {1: "colour"}, inplace = True)
    taxon_c = taxon_c.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_taxon_col, taxon_col = list(taxon_c.iloc[:,0]), \
                                list(taxon_c.iloc[:,1])
    taxon_col = [x + 1 if x == 0  else x for x in taxon_col]
    
    taxa_taxon_c_col = {taxa_taxon_c_cols: taxon_cols for taxa_taxon_c_cols, \
                        taxon_cols in zip(taxa_taxon_col, taxon_col)}
    
    ###########################################################################
    # Obtain bold value for taxon title value of 0 or 1 from Input files.
    taxon_b = data.iloc[15:16,1::].transpose()
    taxon_b = taxon_b.drop("Depth")
    
    if zones_on_off == "off":
        taxon_b = taxon_b.drop("Zones")
        
    taxon_b = taxon_b.reset_index()
    taxon_b.rename(columns = {"index": "TAXA"}, inplace = True)
    taxon_b.rename(columns = {1: "bold"}, inplace = True)
    taxon_b = taxon_b.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_taxon_bold, taxon_bold = list(taxon_b.iloc[:,0]), \
                                  list(taxon_b.iloc[:,1])
    taxa_taxon_b_bold = {taxa_taxon_bolds: taxon_bolds for taxa_taxon_bolds, \
                         taxon_bolds in zip(taxa_taxon_bold, taxon_bold)}
    
    ###########################################################################
    # Obtain vertical spine width value for taxon from input files. If
    # required suggest values between 0.5 and 2.
    plot_vsw = data.iloc[16:17,1::].transpose()
    plot_vsw = plot_vsw.drop("Depth")
    
    if zones_on_off == "off":
        plot_vsw = plot_vsw.drop("Zones")
        
    plot_vsw = plot_vsw.reset_index()
    plot_vsw.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_vsw.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_vsw = plot_vsw.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_vsw, taxon_plot_vsw = list(plot_vsw.iloc[:,0]), \
                                    list(plot_vsw.iloc[:,1])
    taxa_plot_vs_width = {taxa_plot_vsws: taxon_plot_vsws for \
                          taxa_plot_vsws, taxon_plot_vsws in \
                          zip(taxa_plot_vsw, taxon_plot_vsw)}
    
    ###########################################################################
    # Obtain vertical spine style value for taxon from Input files. If
    # required values between 1-4 see manual for codes.
    plot_vsty = data.iloc[17:18,1::].transpose()
    plot_vsty = plot_vsty.drop("Depth")
    
    if zones_on_off == "off":
        plot_vsty = plot_vsty.drop("Zones")
        
    plot_vsty = plot_vsty.reset_index()
    plot_vsty.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_vsty.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_vsty =plot_vsty.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_vsty, taxon_plot_vsty = list(plot_vsty.iloc[:,0]), \
                                      list(plot_vsty.iloc[:,1])
    taxa_plot_vstyle = {taxa_plot_vstys: taxon_plot_vstys for \
                        taxa_plot_vstys, taxon_plot_vstys in \
                        zip(taxa_plot_vsty, taxon_plot_vsty)}
    
    ###########################################################################
    # Obtain vertical spine colour value for taxon from input files if
    # required values between 1-23. See manual for colour codes.
    plot_vs_col = data.iloc[18:19,1::].transpose()
    plot_vs_col = plot_vs_col.drop("Depth")
    
    if zones_on_off == "off":
        plot_vs_col = plot_vs_col.drop("Zones")
        
    plot_vs_col =plot_vs_col.reset_index()
    plot_vs_col.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_vs_col.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_vs_col = plot_vs_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_vs_col, taxon_plot_vs_col = list(plot_vs_col.iloc[:,0]), \
                                          list(plot_vs_col.iloc[:,1])
    taxa_plot_vs_colour = {taxa_plot_vs_cols:taxon_plot_vs_cols for \
                           taxa_plot_vs_cols, taxon_plot_vs_cols \
                           in zip(taxa_plot_vs_col, taxon_plot_vs_col)}
    
    ###########################################################################
    # Obtain left spine width value for taxon from Input files. If rquired
    # suggest values between 0.5 and 2.
    plot_lsw = data.iloc[19:20,1::].transpose()
    plot_lsw = plot_lsw.drop("Depth")
    
    if zones_on_off == "off":
        plot_lsw = plot_lsw.drop("Zones")
        
    plot_lsw = plot_lsw.reset_index()
    plot_lsw.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_lsw.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_lsw = plot_lsw.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_lsw, taxon_plot_lsw = list(plot_lsw.iloc[:,0]), \
                                    list(plot_lsw.iloc[:,1])
    taxa_plot_ls_width = {taxa_plot_lsws:taxon_plot_lsws for \
                          taxa_plot_lsws, taxon_plot_lsws in \
                          zip(taxa_plot_lsw, taxon_plot_lsw)}
      
    ###########################################################################
    # Obtain left spine style value for taxon from Input files.
    plot_lsty = data.iloc[20:21,1::].transpose()
    plot_lsty = plot_lsty.drop("Depth")
    
    if zones_on_off == "off":
        plot_lsty = plot_lsty.drop("Zones")
        
    plot_lsty = plot_lsty.reset_index()
    plot_lsty.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_lsty.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_lsty = plot_lsty.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_lsty, taxon_plot_lsty = list(plot_lsty.iloc[:,0]), \
                                      list(plot_lsty.iloc[:,1])
    taxa_plot_lstyle = {taxa_plot_lstys: taxon_plot_lstys for \
                        taxa_plot_lstys, taxon_plot_lstys in \
                        zip(taxa_plot_lsty, taxon_plot_lsty)}
    
    ###########################################################################
    # Obtain left spine colour value for taxon from Input files. If required 
    # values between 1 - 23. See manual for colour codes.
    plot_ls_col= data.iloc[21:22,1::].transpose()
    plot_ls_col= plot_ls_col.drop("Depth")
    
    if zones_on_off == "off":
        plot_ls_col= plot_ls_col.drop("Zones")
        
    plot_ls_col=plot_ls_col.reset_index()
    plot_ls_col.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_ls_col.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_ls_col= plot_ls_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_ls_col, taxon_plot_ls_col= list(plot_ls_col.iloc[:,0]), \
                                         list(plot_ls_col.iloc[:,1])
    taxa_plot_ls_colour = {taxa_plot_ls_cols: taxon_plot_ls_cols \
                           for taxa_plot_ls_cols, taxon_plot_ls_cols \
                           in zip(taxa_plot_ls_col, taxon_plot_ls_col)}
    
    ###########################################################################
    # Obtain right spine width value for taxon from Input files. If required 
    # suggest values between 0.5 and 2.
    plot_rsw = data.iloc[22:23,1::].transpose()
    plot_rsw = plot_rsw.drop("Depth")
    
    if zones_on_off == "off":
        plot_rsw = plot_rsw.drop("Zones")
        
    plot_rsw = plot_rsw.reset_index()
    plot_rsw.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_rsw.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_rsw = plot_rsw.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rsw, taxon_plot_rsw = list(plot_rsw.iloc[:,0]), \
                                    list(plot_rsw.iloc[:,1])
    taxa_plot_rs_width = {taxa_plot_rsws: taxon_plot_rsws for \
                          taxa_plot_rsws, taxon_plot_rsws in \
                          zip(taxa_plot_rsw, taxon_plot_rsw)}
    
    ###########################################################################
    # Obtain right spine style value for taxon from Input files. If required 
    # values between 1 - 4. See manual for codes.
    plot_rsty = data.iloc[23:24,1::].transpose()
    plot_rsty = plot_rsty.drop("Depth")
    
    if zones_on_off == "off":
        plot_rsty = plot_rsty.drop("Zones")
        
    plot_rsty =plot_rsty.reset_index()
    plot_rsty.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_rsty.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_rsty = plot_rsty.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rsty, taxon_plot_rsty = list(plot_rsty.iloc[:,0]), \
                                      list(plot_rsty.iloc[:,1])
    taxa_plot_rstyle = {taxa_plot_rstys: taxon_plot_rstys for \
                        taxa_plot_rstys, taxon_plot_rstys in \
                        zip(taxa_plot_rsty, taxon_plot_rsty)}
    
    ###########################################################################
    # Obtain right spine colour value for taxon from Input files. If required 
    # values between 1 - 23. See manual for colour codes.
    plot_rs_col = data.iloc[24:25,1::].transpose()
    plot_rs_col = plot_rs_col.drop("Depth")
    
    if zones_on_off == "off":
        plot_rs_col = plot_rs_col.drop("Zones")
        
    plot_rs_col =plot_rs_col.reset_index()
    plot_rs_col.rename(columns = {"index": "TAXA"}, inplace = True)
    plot_rs_col.rename(columns = {1: "WIDTH"}, inplace = True)
    plot_rs_col = plot_rs_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rs_col, taxon_plot_rs_col = list(plot_rs_col.iloc[:,0]), \
                                          list(plot_rs_col.iloc[:,1])
    taxa_plot_rs_colour = {taxa_plot_rs_cors: taxon_plot_rs_cors for \
                           taxa_plot_rs_cors, taxon_plot_rs_cors \
                           in zip(taxa_plot_rs_col, taxon_plot_rs_col)}
    
    ###########################################################################
    # Obtain x major tick colour value for taxon from Input files. If required 
    # values between 1 - 23. See manual for colour codes black is 1.
    x_tick_maj_col = data.iloc[25:26,1::].transpose()
    x_tick_maj_col = x_tick_maj_col.drop("Depth")
    
    if zones_on_off == "off":
        x_tick_maj_col = x_tick_maj_col.drop("Zones")
        
    x_tick_maj_col = x_tick_maj_col.reset_index()
    x_tick_maj_col.rename(columns = {"index": "TAXA"}, inplace = True)
    x_tick_maj_col.rename(columns = {1: "WIDTH"}, inplace = True)
    x_tick_maj_col = x_tick_maj_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rs_col, taxon_plot_rs_col = list(x_tick_maj_col.iloc[:,0]), \
                                          list(x_tick_maj_col.iloc[:,1])
    taxa_x_tick_maj_colour = {taxa_x_tick_maj_cols: taxon_x_tick_maj_cols for \
                              taxa_x_tick_maj_cols, taxon_x_tick_maj_cols \
                              in zip(taxa_plot_rs_col, taxon_plot_rs_col)}
    
    ###########################################################################
    # Obtain x minor tick colour value for taxon from Input files. if required 
    # values between 1 - 23. See manual for colour codes black is 1.
    x_tick_min_col = data.iloc[26:27,1::].transpose()
    x_tick_min_col = x_tick_min_col.drop("Depth")
    
    if zones_on_off == "off":
        x_tick_min_col = x_tick_min_col.drop("Zones")
        
    x_tick_min_col = x_tick_min_col.reset_index()
    x_tick_min_col.rename(columns = {"index": "TAXA"}, inplace = True)
    x_tick_min_col.rename(columns = {1: "WIDTH"}, inplace = True)
    x_tick_min_col = x_tick_min_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rs_col, taxon_plot_rs_col = list(x_tick_min_col.iloc[:,0]), \
                                          list(x_tick_min_col.iloc[:,1])
    taxa_x_tick_min_colour = {taxa_x_tick_min_cols: taxon_x_tick_min_cols \
                              for taxa_x_tick_min_cols, taxon_x_tick_min_cols \
                              in zip(taxa_plot_rs_col, taxon_plot_rs_col)}
    
    ###########################################################################
    # Obtain y major tick colour value for taxon from Input files. If required 
    # values between 1 - 23. See manual for colour codes black is 1.
    y_tick_maj_col = data.iloc[27:28,1::].transpose()
    y_tick_maj_col = y_tick_maj_col.drop("Depth")
    
    if zones_on_off == "off":
        y_tick_maj_col = y_tick_maj_col.drop("Zones")
        
    y_tick_maj_col = y_tick_maj_col.reset_index()
    y_tick_maj_col.rename(columns = {"index": "TAXA"}, inplace = True)
    y_tick_maj_col.rename(columns = {1: "Y MAJ col"}, inplace = True)
    y_tick_maj_col = y_tick_maj_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rs_col, taxon_plot_rs_col = list(y_tick_maj_col.iloc[:,0]), \
                                          list(y_tick_maj_col.iloc[:,1])
    taxa_y_tick_maj_colour = {taxa_y_tick_maj_cols: taxon_y_tick_maj_cols \
                              for taxa_y_tick_maj_cols, taxon_y_tick_maj_cols \
                              in zip(taxa_plot_rs_col, taxon_plot_rs_col)}
    
    ###########################################################################
    # Obtain y minor tick colour value for taxon from Input files. If required 
    # values between 1 - 23. See manual for colour codes black is 1.
    y_tick_min_col = data.iloc[28:29,1::].transpose()
    y_tick_min_col = y_tick_min_col.drop("Depth")
    
    if zones_on_off == "off":
        y_tick_min_col = y_tick_min_col.drop("Zones")
        
    y_tick_min_col = y_tick_min_col.reset_index()
    y_tick_min_col.rename(columns = {"index": "TAXA"}, inplace = True)
    y_tick_min_col.rename(columns = {1: "Y min col"}, inplace = True)
    y_tick_min_col = y_tick_min_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_rs_col, taxon_plot_rs_col = list(y_tick_min_col.iloc[:,0]), \
                                          list(y_tick_min_col.iloc[:,1])
    taxa_y_tick_min_colour = {taxa_y_tick_min_cols: taxon_y_tick_min_cols for \
                              taxa_y_tick_min_cols, taxon_y_tick_min_cols in \
                              zip(taxa_plot_rs_col, taxon_plot_rs_col)}
    
    ###########################################################################
    # Obtain whether taxa is to have exaggeration or not from Input file. 0 is
    # no exaggeration, any other number is number to multiply original to get 
    # exaggeration.
    exag = data.iloc[29:30,1::].transpose()
    exag = exag.drop("Depth")
    
    if zones_on_off == "off":
        exag = exag.drop("Zones")
        
    exag = exag.reset_index()
    exag.rename(columns = {"index":"TAXA"}, inplace = True)
    exag.rename(columns = {1:"exag"}, inplace = True)
    exag.rename(columns = {29:"exag"}, inplace = True)
    #exag = exag.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag, taxon_plot_exag = list(exag.iloc[:,0]), \
                                      list(exag.iloc[:,1])
    taxa_exag = {taxa_plot_exags: taxon_plot_exags for taxa_plot_exags, \
                 taxon_plot_exags in zip(taxa_plot_exag, taxon_plot_exag)}
    
    taxa_exag_1 = taxa_exag.copy() 
    ###########################################################################
    # If exaggeration is required this dictates the type, either graph type 3 
    # or 4 is permitted. Obtain from Input file.
    exag_type = data.iloc[30:31,1::].transpose()
    exag_type = exag_type.drop("Depth")
    
    if zones_on_off == "off":
        exag_type = exag_type.drop("Zones")
        
    exag_type = exag_type.reset_index()
    exag_type.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_type.rename(columns = {1: "exag_type"}, inplace = True)
    exag_type = exag_type.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_type, taxon_plot_exag_type = list(exag_type.iloc[:,0]), \
                                                list(exag_type.iloc[:,1])
    taxa_exag_type = {taxa_plot_exags_type: taxon_plot_exags_type for \
                      taxa_plot_exags_type, taxon_plot_exags_type in \
                      zip(taxa_plot_exag_type, taxon_plot_exag_type)}
    
    ###########################################################################
    # Obtain colour code of exaggeration fill from Input file. If required
    # values between 1 - 23. See manual for colour codes black is 1.
    exag_col = data.iloc[31:32,1::].transpose()
    exag_col = exag_col.drop("Depth")
    
    if zones_on_off == "off":
        exag_col = exag_col.drop("Zones")
        
    exag_col = exag_col.reset_index()
    exag_col.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_col.rename(columns = {1: "exag col"}, inplace = True)
    exag_col = exag_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_col, taxon_plot_exag_col = list(exag_col.iloc[:,0]), \
                                              list(exag_col.iloc[:,1])
    taxa_exag_col = {taxa_plot_exags_col: taxon_plot_exags_col for \
                     taxa_plot_exags_col, taxon_plot_exags_col in \
                     zip(taxa_plot_exag_col, taxon_plot_exag_col)}
    
    ###########################################################################
    # Obtain transparency of exaggeration fill from Input file. If required
    # values between 0 - 1. 0 fully tranparent, 1 not at all transparent.
    exag_trans = data.iloc[32:33,1::].transpose()
    exag_trans = exag_trans.drop("Depth")
    
    if zones_on_off == "off":
        exag_trans = exag_trans.drop("Zones")
        
    exag_trans = exag_trans.reset_index()
    exag_trans.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_trans.rename(columns = {1: "EXAG TRANS"}, inplace = True)
    exag_trans = exag_trans.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_trans, taxon_plot_exag_trans = list(exag_trans.iloc[:,0]), \
                                                  list(exag_trans.iloc[:,1])
    taxa_exag_trans = {taxa_plot_exags_trans: taxon_plot_exags_trans for \
                       taxa_plot_exags_trans, taxon_plot_exags_trans in \
                       zip(taxa_plot_exag_trans, taxon_plot_exag_trans)}
    
    ###########################################################################
    # Obtain colour code of exaggeration line from Input file, if required
    # values  between 1 - 23. See manual for colour codes black is 1.
    exag_line_col = data.iloc[33:34,1::].transpose()
    exag_line_col = exag_line_col.drop("Depth")
    
    if zones_on_off == "off":
        exag_line_col = exag_line_col.drop("Zones")
        
    exag_line_col = exag_line_col.reset_index()
    exag_line_col.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_line_col.rename(columns = {1: "EXAG_LINE_COL"}, inplace = True)
    exag_line_col = exag_line_col.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_line_col, taxon_plot_exag_line_col \
                             = list(exag_line_col.iloc[:,0]), \
                               list(exag_line_col.iloc[:,1])
    taxa_exag_line_col = {taxa_plot_exags_line_col:taxon_plot_exags_line_col \
                          for taxa_plot_exags_line_col, \
                          taxon_plot_exags_line_col in zip \
                          (taxa_plot_exag_line_col, \
                           taxon_plot_exag_line_col)}
    
    ###########################################################################
    # Obtain line width for exaggeration line from Input file. If required
    # suggest values between 0.5 and 2.
    exag_lw = data.iloc[34:35,1::].transpose()
    exag_lw = exag_lw.drop("Depth")
    
    if zones_on_off == "off":
        exag_lw = exag_lw.drop("Zones")
        
    exag_lw = exag_lw.reset_index()
    exag_lw.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_lw.rename(columns = {1: "EXAG LW"}, inplace = True)
    exag_lw = exag_lw.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_lw, taxon_plot_exag_lw = list(exag_lw.iloc[:,0]), \
                                            list(exag_lw.iloc[:,1])
    taxa_exag_lw = {taxa_plot_exags_lw: taxon_plot_exags_lw for \
                    taxa_plot_exags_lw, taxon_plot_exags_lw in \
                    zip(taxa_plot_exag_lw, taxon_plot_exag_lw)}
    
    ###########################################################################
    # Obtain line style for exaggeration line from Input File. If required
    # values between 1 - 4. See manual for codes.
    exag_ls = data.iloc[35:36,1::].transpose()
    exag_ls = exag_ls.drop("Depth")
    
    if zones_on_off == "off":
        exag_ls = exag_ls.drop("Zones")
        
    exag_ls = exag_ls.reset_index()
    exag_ls.rename(columns = {"index": "TAXA"}, inplace = True)
    exag_ls.rename(columns = {1: "exag LS"}, inplace = True)
    exag_ls = exag_ls.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_exag_ls, taxon_plot_exag_ls = list(exag_ls.iloc[:,0]), \
                                            list(exag_ls.iloc[:,1])
    taxa_exag_ls = {taxa_plot_exags_ls: taxon_plot_exags_ls for \
                    taxa_plot_exags_ls, taxon_plot_exags_ls in \
                    zip(taxa_plot_exag_ls, taxon_plot_exag_ls)}
    
    ###########################################################################
    # Obtain whether stack plot 1 is required from Input file.
    stack_plot_1 = data.iloc[36:37,1::].transpose()
    stack_plot_1 = stack_plot_1.drop("Depth")
    
    if zones_on_off == "off":
        stack_plot_1 = stack_plot_1.drop("Zones")
        
    stack_plot_1 = stack_plot_1.reset_index()
    stack_plot_1.rename(columns = {"index": "TAXA"}, inplace = True)
    stack_plot_1.rename(columns = {1: "STACK_Y_N"}, inplace = True)
    stack_plot_1 = stack_plot_1.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_stack_plot_1, taxon_plot_stack_plot_1 = \
                           list(stack_plot_1.iloc[:,0]), \
                           list(stack_plot_1.iloc[:,1])
    taxa_stack_plot_1 = {taxa_plot_1_stacks_plot: taxon_plot_1_stacks_plot \
                         for taxa_plot_1_stacks_plot, \
                             taxon_plot_1_stacks_plot \
                         in zip(taxa_plot_stack_plot_1, \
                                taxon_plot_stack_plot_1)}
    
    # Find unique values of stack plot groupings and remove zero values
    stack_plot_1_uni = np.unique(taxon_plot_stack_plot_1)
    stack_plot_1_uni = list(stack_plot_1_uni)
    if 0.0 in stack_plot_1_uni:
        stack_plot_1_uni.remove(0.0)
    
    ###########################################################################
    # Obtain whether stack plot 2 is required from Input file.
    stack_plot_2 = data.iloc[37:38,1::].transpose()
    stack_plot_2 = stack_plot_2.drop("Depth")
    
    if zones_on_off == "off":
        stack_plot_2 = stack_plot_2.drop("Zones")
        
    stack_plot_2 = stack_plot_2.reset_index()
    stack_plot_2.rename(columns = {"index": "TAXA"}, inplace = True)
    stack_plot_2.rename(columns = {1: "exag LS"}, inplace = True)
    stack_plot_2 = stack_plot_2.sort_values("TAXA")
    
    # Create dictionary of above.
    taxa_plot_stack_plot_2, taxon_plot_stack_plot_2 \
                            = list(stack_plot_2.iloc[:,0]), \
                              list(stack_plot_2.iloc[:,1])
    taxa_stack_plot_2 = {taxa_plot_2_stacks_plot: taxon_plot_2_stacks_plot \
                         for taxa_plot_2_stacks_plot, \
                             taxon_plot_2_stacks_plot \
                         in zip(taxa_plot_stack_plot_2, \
                                taxon_plot_stack_plot_2)}
    
    # Find unique values of stack plot groupings and remove zero values
    stack_plot_2_uni = np.unique(taxon_plot_stack_plot_2)
    stack_plot_2_uni = list(stack_plot_2_uni)
    if 0.0 in stack_plot_2_uni:
        stack_plot_2_uni.remove(0.0)
    
    ###########################################################################
    ###########################################################################
    # Create a set of values to 'scale' the y axis of each plot correctly, 
    # 'the abundance' axis. To do this the program needs to know if any non 
    # standard scaling graphs are required before can do this. This is done
    # with a  list of non std 
    non_std_scaling_1 = str(par_dict["NSC 1**"]).strip()
    non_std_scaling_2 = str(par_dict["NSC 2**"]).strip()
    non_std_scaling_3 = str(par_dict["NSC 3**"]).strip()
    non_std_scaling_4 = str(par_dict["NSC 4**"]).strip()
    non_std_scaling_5 = str(par_dict["NSC 5**"]).strip()
    
    non_std_list = [non_std_scaling_1, non_std_scaling_2, non_std_scaling_3, \
                           non_std_scaling_4, non_std_scaling_5]
    non_std_list = ["none" if x == "NONE" else x for x in non_std_list]
    
    non_std_list = [x for x in non_std_list if x != "none" and \
                    pd.isnull(x) == False]
    
    # Find the minimum value for each taxa in data and the taxa names
    min_list = list(data.iloc[38:,2:].min())
    taxa_list = list(data.iloc[0:,2:])
     
    # Create a dummy diff list with all elements to update later to preserve 
    # the order. This list here is taxa and the minimum values
    diff_list_ratios_dict = {k: v for k, v in zip(taxa_list, min_list)}
     
    # Create another list as above and call it min_taxa_dict
    min_taxa_dict = {k: v for k, v in zip(taxa_list, min_list)}
    
    # Create another list as above and call it min_taxa_dict and use if non std 
    # scaling elements are requested
    min_taxa_dict_1 = {k: v for k, v in zip(taxa_list, min_list)}
    
    # Remove non std scaling elements from min taxa dict so not used later for 
    # scaling of plots for other taxa
    for x in non_std_list:
        min_taxa_dict_1.pop(x)
    
    # Create list of minimum taxa values without non std scaling elements
    min_list = [x for x in min_taxa_dict_1.values()]
    
    # If zones have not been specified this value is removed
    if zones_on_off == "off":
        min_list = min_list[:-1]
    
    # Reverse the order of minimum values list and round the value
    min_list = min_list[::-1] 
    min_list_round = list(np.round(min_list, decimals = -1))
    
    # Determine the minimum of all minimum abundance values
    min_list_min = np.round(min(min_list), decimals = -1)
    
    # Determine maximum values for each taxa
    max_list = list(data.iloc[38:,2:].max())
    
    # If zones are not specified remove from list of maximum values  
    if zones_on_off == "off":
        max_list = max_list[:-1]
    
    # Create dictionaries of taxa and maximum values
    max_taxa_dict = {k: v for k, v in zip(taxa_list, max_list)}
    max_taxa_dict_1 = {k: v for k, v in zip(taxa_list, max_list)}
    
    # Remove non std scaling elements from min taxa dict so not used later for 
    # scaling of plots for other taxa
    for x in non_std_list:
        max_taxa_dict_1.pop(x)
    # Remove non std scaling elements from taxa exageration dictionary
    for x in non_std_list:
        taxa_exag_1.pop(x)
    
    # Create a list of maximum taxa values and get the maximum of all maximum 
    # values
    max_list = [v for v in max_taxa_dict_1.values()]    
    max_list_round = np.round(max_list, decimals = -1)
    max_list_max = np.round(max(max_list), decimals = -1)
    
    # Find ratios of the max of each taxa to the max of all maximums 
    max_list_ratios = [x / max_list_max for x in max_list]
    max_list_ratios = max_list_ratios[::-1]
    max_list_round = max_list_round[::-1]
    max_list = max_list[::-1]
    
    # Create taxa lists from maximum list
    taxa_list = list(max_taxa_dict_1.keys())
    taxa_list = taxa_list[::-1]
    
    # Account for whether exaggerations are requested. If they are create a 
    # new maximum list
    if exag["exag"].max() > 0: 
        new_max_list = [] 
        taxa_exag_1_v = list(taxa_exag_1.values())
        taxa_exag_1_v.reverse()
        
        # For exaggerated taxa make the max value greater so very low values
        # can be seen more easily on the plots. Here we add 20. Could be 
        # adjusted here if user does not like that. Can be increased or 
        # decreased but this appears  the best compromise
        for x, y in zip(max_list, taxa_exag_1_v):
    
            if x < 20 and y > 0:
                new_max_list.append(x + 20)
            else:
                new_max_list.append(x)
        
        # Create a diff list. List of the difference between max and min 
        # values here for data with exaggeration specified and create a new
        # maximum taxa value dictionary
        diff_list = [x - y for x, y in zip(new_max_list, min_list)]
        new_max_taxa_dict = {k: v for k, v in zip(taxa_list, new_max_list)}
        
    # If no exaggeration specified craete a diff list with previous variables
    # and a maximum taxa value dictionary.
    else:
        diff_list = [x - y for x, y in zip(max_list, min_list)]
        max_taxa_dict = {k: v for k, v in zip(taxa_list, max_list)}
    
    # Create variable of the maximum diff between min and max values    
    diff_list_max = np.round(max(diff_list),decimals = -1)
    
    # Create list of ratios of diff between min and max and max diff. This and 
    # later variants are used for the plot width scaling for each taxa plot
    diff_list_ratios = [x / diff_list_max for x in diff_list]
    diff_list_ratios_dict_1 = {k: v for k, v in zip(taxa_list, \
                                                    diff_list_ratios)}
    diff_list_ratios_dict.update(diff_list_ratios_dict_1)
    
    min_list = list(data.iloc[38:,2:].min())
    min_list_round = list(np.round(min_list,decimals = - 1))
    min_list = min_list[::-1]
    min_list_round = min_list_round[::-1]
    
    ###########################################################################
    ###########################################################################
    # Remove plot style and colour indexes from the Input file and Extra Input 
    # file if specified ready for plotting.
    data_2 = data.drop(np.arange(0, 38, 1), axis = 0)
    
    if extra_yn != "none":
        data_extra_2 = data_extra.drop(np.arange(0, 36, 1), axis = 0)
    
    ###########################################################################
    ###########################################################################
    # Read in groups for stack plots if stack plots are required.
    stack_plot_1_on_off = par_dict["Stack plot 1 on/off**"]. \
                                  strip().lower()
    stack_plot_2_on_off = par_dict["Stack plot 2 on/off**"]. \
                                  strip().lower()
    
    # Obtain parameters for stack plot 1 if required and error check entries.
    if pd.isnull(stack_plot_1_on_off) == True or stack_plot_1_on_off not in \
        ["on", "off"]:
        print("\nStack plot 1 on/off in Parameter file "
              "requires an entry of 'on' or 'off'.")
        sys.exit()
        
    if stack_plot_1_on_off == "on":
        
        if max(taxa_stack_plot_1.values()) <= 0:
            print("\nStack plot 1 has been requested in the "
                  "the Parameter file but there is no groupings in the input "
                  "file.")
            sys.exit()
            
        try:
            stack_plot_1_title = par_dict \
            ["Stack plot title 1"].strip()
            
            if pd.isnull(stack_plot_1_title) == True:
                print("\nStack plot title 1 entry in Parameter file "
                      "is empty. Is an entry required ?")
        except:
            print("\nStack plot title 1 entry in Parameter file is "
                  "missing or incorrect.")
            sys.exit()
            
        # Check colour entries in Parameter file when provided as list.
        try:
            stack_plot_1_colours = par_dict["Stack plot col list "
                                           "1"].replace(" ","").split(",")
            stack_plot_1_colours = [float(x) for x in stack_plot_1_colours]
            
        except:
            print("\nEntry for Stack plot col list 1 in Parameter "
                  "file is missing or incorrect.")
            sys.exit()
            
        if any(pd.isnull(stack_plot_1_colours)) == False:
            if any (i < 0 or i > col_max for i in stack_plot_1_colours):
                print("\n A colour entry for Stack plot col list in "
                      "Parameter file is out of bounds.")
                sys.exit()
                
        # Check stack plot size entry
        try:
            stack_plot_1_size = float(par_dict["Stack plot size 1"])
            
            if pd.isnull(stack_plot_1_size) == True:
                print("\nStack plot 1 entry in Parameter file is "
                      "required.")
                sys.exit()
        except:
            print("\nStack plot size 1 entry in Parameter file is "
                  "missing or incorrect.")
            sys.exit()
            
        # Check stack plot line width and colour entry          
        try:
            stack_plot_1_lw = float(par_dict \
                                   ["Stack plot line width 1"])
                
            if pd.isnull(stack_plot_1_lw) == False:
                
                try:
                    stack_plot_1_line_colour = float(par_dict\
                                                    ["Stack "
                                                    "plot line colour 1"])
    
                    if stack_plot_1_line_colour < 0 or \
                       stack_plot_1_line_colour > col_max or \
                       pd.isnull(stack_plot_1_line_colour) == True:
                        print("\nStack plot line colour 1 entry in "
                              "Parameter file is missing or out of bounds.")
                        sys.exit()
                except:
                    print("\nStack plot line colour 1 entry in "
                          "Parameter file is missing or incorrect.")
                    sys.exit()
        except:
            print("\nStack plot line width 1 entry in Parameter file "
                  "is missing or incorrect if not required use zero as entry.")
            sys.exit()
            
        stack_plot_1_line_colour = float(par_dict["Stack "
                                                 "plot line colour 1"])
        
        if stack_plot_1_line_colour <= 0 or stack_plot_1_line_colour > \
                col_max:
            print("\nStack plot line colour 1 entry in Parameter file "
                  "is missing or incorrect.")
            sys.exit()
    
        stack_plot_1_yn = par_dict["Stack plot title 1"].strip()
    
        # Check stack plot calculation entry
        try:
            stack_calc_1 = par_dict["Stack plot calculation 1"]. \
                                  strip().lower()
                                  
            if pd.isnull(stack_calc_1) == True or stack_calc_1 not in \
                    ["yes","no"]:
                print("\nEntry for Stack plot calculation 1 is "
                      "required. Entry should be yes or no.")
                sys.exit()
                
        except:
            print("\nEntry for Stack plot calculation 1 entry in the "
                  "Parameter file is missing or incorrect.") 
            sys.exit()
            
        if len(stack_plot_1_colours) != len(stack_plot_1_uni):
            print("\nNumber of Stack 1 plot groups are different to "
                  "number of colours prescribed in Parameter file.")
            sys.exit()
    
    # Obtain parameters for stack plot 2 if required and error check entries.
    if stack_plot_2_on_off == "on":
        if max(taxa_stack_plot_2.values()) <= 0:
            print("\nStack plot 2 has been requested in the "
                  "Parameter file but there is no groupings in the input "
                  "file.")
            sys.exit()
            
        # Error check stack plot 2 title entry
        try:
            stack_plot_2_title = par_dict \
            ["Stack plot title 2"].strip()
            
            if pd.isnull(stack_plot_2_title) == True:
                print("\nStack plot title 2 entry is empty. Is an "
                      "entry required ?")
                sys.exit()
                
        except:
            print("\nStack plot title 2 entry in Parameter file is "
                  "missing or incorrect.")
            sys.exit()
            
        # Check stack plot 2 colour entries in Parameter file when provided as 
        # list.
        try:
            stack_plot_2_colours = par_dict["Stack plot col "
                                           "list 2"].replace(" ","") \
                                                    .split(",")
            stack_plot_2_colours = [float(x) for x in stack_plot_2_colours]
            
            if any(pd.isnull(stack_plot_2_colours)) == False:
                if any (i < 0 or i > col_max for i in stack_plot_2_colours):
                    print("\nA colour entry for Zone line col list in"
                          " Parameter file is out of bounds.")
                    sys.exit()
                    
        except:
            print("\nEntry for Stack plot col list 2 in Parameter "
                  "file is missing or incorrect. Make sure all required"
                  " entries are filled.")
            sys.exit()
        
        # Check stack plot 2 size entry
        try:
            stack_plot_2_size = float(par_dict["Stack plot size 2"])
            if pd.isnull(stack_plot_2_size) == True:
                print("\nStack plot 2 entry in Parameter file is "
                      "required.")
                sys.exit()
                
        except:
            print("\nStack plot size 2 entry in Parameter file is "
                  "missing or incorrect.")
            sys.exit()
            
        # Check stack plot 2 line width and colour entry
        try:
            stack_plot_2_lw = float(par_dict \
                                   ["Stack plot line width 2"])
            if pd.isnull(stack_plot_2_lw) == False:
                try:
                    stack_plot_2_line_colour = float(par_dict\
                                                    ["Stack "
                                                    "plot line colour 2"])
                        
                    if stack_plot_2_line_colour < 0 or \
                        stack_plot_2_line_colour > col_max or \
                        pd.isnull(stack_plot_2_line_colour) == True:
                        print("\nStack plot line colour 2 in "
                              "Parameter file is missing or out of bounds.")
                        sys.exit()
                        
                except:
                    print("\nStack plot line colour 2 entry in "
                          "Parameter file is missing or incorrect.")
                    sys.exit()
        except:
            print("\nStack plot line width 2 entry in Parameter file "
                  "is missing or incorrect if not required use zero as entry.")
            sys.exit()
    
        stack_plot_2_line_colour = float(par_dict["Stack "
                                                 "plot line colour 2"])
    
        if stack_plot_2_line_colour <= 0 or stack_plot_2_line_colour > \
                col_max:
            print("\nStack plot line colour 2 entry in Parameter file "
                  "is missing or incorrect.")
            sys.exit()
    
        stack_plot_2_yn = par_dict["Stack plot title 2"].strip()
        
        # Check stack plot 2 calculation entry
        try:
            stack_calc_2 = par_dict["Stack plot calculation 2"]. \
                                  strip().lower()
                                  
            if pd.isnull(stack_calc_2) == True or stack_calc_2 not in \
                    ["yes","no"]:
                print("\nEntry for Stack plot calculation 2 in "
                      "Parameter file is required. Entry should be 'yes' or "
                      "'no'.")
                sys.exit()
        except:
            print("\nEntry for Stack plot calculation 2 entry in "
                  "Parameter file is missing or incorrect.") 
            sys.exit()
    
        if len(stack_plot_2_colours) != len(stack_plot_2_uni):
            print("\nNumber of Stack 2 plot groups are different to "
                  "number of colours prescribed in Parameter file.")
            sys.exit()
    
    # Determine number of stack plots asked for by user 0, 1 or 2. Employed
    # later in program 
    stack_plots_yn = [stack_plot_1_on_off, stack_plot_2_on_off]
    num_stack_plots = sum([1 if x !="off" and pd.isnull(x) == False \
                          else 0 for x in stack_plots_yn])
        
    # Create marker for stack plots ready for later in the program
    num_stack = 1
    
    # Stack plot 1 must be used if only one is specified. Can not have one 
    # instance and use the Stack plot 2 entries in the Paramater file so error 
    # message is given if that happens.
    if num_stack_plots > 0 and stack_plot_1_on_off =="off":
        print("\nUse available Stack plot 1 entries before "
              "Stack plot 2 entries if only one Stack plot "
              "required.")
        sys.exit()
    
    # Prep data for later stack plots if required. Has palaeo data and stack 
    # groupings for Stack plots 1 and 2
    if num_stack_plots > 0:
        data_3 = data.drop(np.arange(0, 36, 1),axis = 0) 
        data_3 = data_3.transpose()
        data_3 = data_3.drop(["Unnamed: 0"], axis = 0)
        data_3 = data_3.rename(columns=data_3.iloc[0])
        data_stack_1 = list(data_3.iloc[::,0])
        data_stack_2 = list(data_3.iloc[::,1])
        
    ###########################################################################
        # Stack plot 1 can have up to 5 groups. Can expand this if required by
        # adding extra code.
        
        # Find number of taxa and depth
        length = len(data_3.columns)
        
        # Create empty lists for each possible stack group for Stack plot 1. 
        # Limited to 5 groups at present. Can be expanded with additional code.
        if stack_plot_1_on_off == "on":
            stack_1_sums_1 = []
            stack_1_sums_2 = []
            stack_1_sums_3 = []
            stack_1_sums_4 = []
            stack_1_sums_5 = []
        
            # Create a ratio for the stack plot so is correctly scaled 
            # on y axis. The initial size is goverened by max value in the 
            # column used in the input file and then adjusted by size
            # specified in  parameter file by user
            diff_list_ratios_dict[stack_plot_1_title] = 1 * (stack_plot_1_size)
            
            a = 2
            
            # Get data for stack plots and error check.
            for x in range (length - 2):
                stack_list_1_1, stack_list_1_2, stack_list_1_3, \
                stack_list_1_4, stack_list_1_5 = [],[],[],[],[]
                
                for values, grouping in zip(data_3.iloc[::,a], data_stack_1):
                    if grouping == 1:
                        stack_list_1_1.append(values)
                    if grouping == 2:
                        stack_list_1_2.append(values)
                    if grouping == 3:
                        stack_list_1_3.append(values)
                    if grouping == 4:
                        stack_list_1_4.append(values)
                    if grouping == 5:
                        stack_list_1_5.append(values)
                        
                    if grouping > 5 or pd.isnull(grouping) \
                        == True:
                            print("\nStack plot 1 groupings are "
                                  "limited to 5 groups maximim at present. "
                                  "Error in grouping numbers. If not required"
                                  " add a zero.")
                            sys.exit()
    
                stack_1_sums_1.append(sum(stack_list_1_1))
                stack_1_sums_2.append(sum(stack_list_1_2))
                stack_1_sums_3.append(sum(stack_list_1_3))
                stack_1_sums_4.append(sum(stack_list_1_4))
                stack_1_sums_5.append(sum(stack_list_1_5))
                
                a += 1
    
            # If percentage calculations are required (ie the groups of data 
            # do not add up to 100. Does not matter but if the user want to 
            # re calculate so they do is carried out here).
            if stack_calc_1 == "yes":
                stack_1_list = [stack_1_sums_1, stack_1_sums_2, \
                                stack_1_sums_3, stack_1_sums_4, stack_1_sums_5]
                
                stack_1_all_sum = [v + w + x + y + z for v, w, x, y, z \
                                  in zip(stack_1_sums_1, stack_1_sums_2, \
                                         stack_1_sums_3, stack_1_sums_4, \
                                         stack_1_sums_5)]
                
                stack_1_sums_1_calc = []
                stack_1_sums_2_calc = []
                stack_1_sums_3_calc = []
                stack_1_sums_4_calc = []
                stack_1_sums_5_calc = []
                
                stack_1_list_calc = [stack_1_sums_1_calc, \
                                     stack_1_sums_2_calc, \
                                     stack_1_sums_3_calc, \
                                     stack_1_sums_4_calc, \
                                     stack_1_sums_5_calc]
                
                for w, x in zip(stack_1_list, stack_1_list_calc):
                    for y, z in zip(w, stack_1_all_sum):
                        x.append(y/z * 100)
    
    ###########################################################################
        # Stack plot 2 can have up to 5 groups as part of the stack 
        # plots. Can expand this if required by adding extra code.
        if stack_plot_2_on_off == "on":
            
            stack_2_sums_1 = []
            stack_2_sums_2 = []
            stack_2_sums_3 = []
            stack_2_sums_4 = []
            stack_2_sums_5 = []
            
            # Create a ratio for the stack plot so is correctly scaled 
            # on y axis.
            diff_list_ratios_dict[stack_plot_2_title] = 1 * \
                (stack_plot_2_size)
        
            a = 2
            
            # Get data for stack plots and error check.
            for x in range (length - 2):
                stack_list_2_1, stack_list_2_2, stack_list_2_3, \
                    stack_list_2_4, stack_list_2_5 = [], [], [], [], []
                
                for values, grouping in zip(data_3.iloc[::,a], data_stack_2):
                    if grouping == 1:
                        stack_list_2_1.append(values)
                    if grouping == 2:
                        stack_list_2_2.append(values)
                    if grouping == 3:
                        stack_list_2_3.append(values)
                    if grouping == 4:
                        stack_list_2_4.append(values)
                    if grouping == 5:
                        stack_list_2_5.append(values) 
                        
                    if grouping > 5 or pd.isnull(grouping) == True:
                            print("\nStack plot 1 groupings are "
                                  "limited to 5 groups maximim at present. "
                                  "Error in grouping numbers. If not required"
                                  " add a zero.")
                            sys.exit()
                            
                stack_2_sums_1.append(sum(stack_list_2_1))
                stack_2_sums_2.append(sum(stack_list_2_2))
                stack_2_sums_3.append(sum(stack_list_2_3))
                stack_2_sums_4.append(sum(stack_list_2_4))
                stack_2_sums_5.append(sum(stack_list_2_5))
            
                a += 1
                
            # If percentage calculations are required (ie the groups of data 
            # do not add up to 100. Does not matter but if the user want to 
            # re calculate so they do is carried out here).
            if stack_calc_2 == "yes":
                stack_2_list = [stack_2_sums_1, stack_2_sums_2, \
                                stack_2_sums_3, stack_2_sums_4, stack_2_sums_5]
                
                stack_2_all_sum = [v + w + x + y + z for v, w, x, y, z \
                                  in zip(stack_2_sums_1, stack_2_sums_2, \
                                         stack_2_sums_3, stack_2_sums_4, \
                                         stack_2_sums_5)]
                
                stack_2_sums_1_calc = []
                stack_2_sums_2_calc = []
                stack_2_sums_3_calc = []
                stack_2_sums_4_calc = []
                stack_2_sums_5_calc = []
                
                stack_2_list_calc = [stack_2_sums_1_calc, \
                                     stack_2_sums_2_calc, \
                                     stack_2_sums_3_calc, \
                                     stack_2_sums_4_calc, \
                                     stack_2_sums_5_calc]
                
                for w, x in zip(stack_2_list, stack_2_list_calc):
                    for y, z in zip(w, stack_2_all_sum):
                        x.append(y/z * 100)
    
    ###########################################################################
    ###########################################################################
    # Obtain axis preferences from Input file such as axis limits, intervals 
    # and font style at present one font style is specified for the 
    # entire plot. More fonts are available in python and can be added to the
    # code. At present the program uses Arial, Calibri, Dejavu sans or
    # Times New Roman.
    
    # Get dictionary entry for text font style and check it.
    try:
        font_style = par_dict["Font style**"].strip().lower()
    except:
        print("\nProblem with font style entry in Parameter file Group 3. "
              "Check entry for format and spelling.")
        sys.exit()
        
    Font_check = ["arial", "calibri", "dejavu sans", "times new roman"]
    
    if font_style not in Font_check:
        print("\nCheck font style entry in Parameter file. Is not one of the"
              " 4 presently available.")
        sys.exit()
        
    # Obtain height and widths of entire figure and check.
    try:
        overall_x = float(par_dict["Overall figure size X**"].replace(" ",""))
        overall_y = float(par_dict["Overall figure size Y**"].replace(" ",""))
    except:
        print("\nProblem with Parameter file Group 2 entry. Check entry."
              " Is it numeric?")
        sys.exit()
    
    # Obtain X and Y axis limits and check.
    try:
        x_limit_top = int(par_dict["X limit top**"].replace(" ","")) 
        x_limit_base = int(par_dict["X limit base**"].replace(" ","")) 
        x_limit_diff = x_limit_base - x_limit_top
    except:
        print("\nProblem with X limit top and X limit base entries in"
              " Parameter file. Check these entries are numeric and not "
              "strings.")
        sys.exit()
    
    ###########################################################################
    # Obtain user specified X and Y tick and interval parameters and check.
    # Obtain space between plots parameter and check.
    try:
        h_space = float(par_dict["Space between plots**"].replace(" ",""))
    except:
        print("\nCheck Space between plots entry in Parameter file. Check"
              " entry and format.")
        sys.exit()
    
    # Obtain axis tick parameter controls from the Parameter file and check.
    try:
        x_major_int = int(par_dict["X major interval**"].replace(" ",""))
        y_major_int_0 = int(par_dict["Y major tick interval**"] \
                            .replace(" ",""))
    except:
        print("\nProblem with X major interval or Y major tick interval in "
              "Parameter file. Check these entries are numeric.")
        sys.exit()
    
    try:
        x_major_tick_len = float(par_dict["X major tick length**"] \
                                 .replace(" ",""))
        y_major_tick_len = float(par_dict["Y major tick length**"] \
                                 .replace(" ",""))
        x_major_tick_wid = float(par_dict["X major tick width**"] \
                                 .replace(" ",""))
        y_major_tick_wid = float(par_dict["Y major tick width**"] \
                                 .replace(" ",""))
    except:
        print("\nProblem with X major tick length, Y major tick length,"
              " X major tick width or Y major tick width in Parameter file."
              " Check these entries are numeric.")
        sys.exit()    
        
    try:
        x_all_ticks = par_dict["X ticks depth axis only**"].replace(" ","") \
                             .lower()
        y_ticks_l_r = par_dict["Y ticks both ends of plot on/off**"] \
                              .replace(" ","").lower()
        x_minor_ticks_on_off = par_dict["X minor ticks on/off**"]. \
                               replace(" ","").lower()
        y_minor_ticks_on_off = par_dict["Y minor ticks on/off**"]. \
                               replace(" ","").lower()
    except:
        print("\nProblem with X ticks depth axis only, Y ticks both ends of "
              "plot on/off, X minor ticks on/off or Y minor ticks on/off"
              " entries in Parameter file. Check these entries are strings"
              " and are either 'on' or 'off'.")
        sys.exit() 
    
    x_y_tick_checks = [x_all_ticks ,y_ticks_l_r, x_minor_ticks_on_off, \
                       y_minor_ticks_on_off ]
    
    if any(i != "on" and i != "off" for i in x_y_tick_checks) == True:
        print("\nProblem with X ticks depth axis only, Y ticks both ends of "
              "plot on/off, X minor ticks on/off or Y minor ticks on/off"
              " entries in Parameter file. Check these entries are strings"
              " and are either 'on' or 'off'.")
        sys.exit() 
    
    # Check entries for x minor parameters if specified and load in parameters.
    if x_minor_ticks_on_off == "on":
        try:
            x_minor_int = int(par_dict["X minor interval"].replace(" ",""))
            x_minor_tick_len = float(par_dict["X minor tick length"]. \
                                     replace(" ",""))
            x_minor_tick_wid = float(par_dict["X minor tick width"]. \
                                     replace(" ",""))
        except:
            print("\nProblem with X minor interval, X minor tick length or X "
                  "minor tick width in Parameter file. Check these entries"
                  " are numeric.")
            sys.exit()         
        
        x_min_par_dict = {k: v for k, v in par_dict.items() \
                          if "X minor" in str(k)}
            
        for k,v in x_min_par_dict.items():
            if pd.isnull(v) == True and k != "Zone X minor tick colour":
                print(f"\nEntry for {k} is missing in Parameter file.")
                sys.exit()
                
    # Check entries for y minor parameters if specified and load in parameters 
    # and check.
    if y_minor_ticks_on_off == "on":
        try:
            y_minor_int_0 = int(par_dict["Y minor tick interval"] \
                                .replace(" ",""))
            y_minor_tick_wid = float(par_dict["Y minor tick width"] \
                                     .replace(" ",""))        
            y_minor_tick_len = float(par_dict["Y minor tick length"] \
                                     .replace(" ","")) 
        except:
            print("\nProblem with Y minor tick interval, Y minor tick width"
                  " or Y minor tick length in Parameter file. Check these"
                  " entries are numeric.")
            sys.exit()     
            
        y_min_par_dict = {k: v for k, v in par_dict.items() \
                          if "Y minor" in str(k)} 
            
        for k,v in y_min_par_dict.items():
            if pd.isnull(v) == True:
                print(f"\nEntry for {k} is missing in Parameter file.")
                sys.exit()    
    
    # Check all required x and y parameters have entries.
    x_y_check_list_1 = [h_space, x_major_int, y_major_int_0, x_all_ticks, \
                        y_ticks_l_r, x_major_tick_len, y_major_tick_len, \
                        x_major_tick_wid, y_major_tick_wid]
        
    if any(i == pd.isnull for i in x_y_check_list_1):
        print("\nMissing value for Group 7 or 8 in Parameter file.")
    
    ###########################################################################
    ###########################################################################
    # Obtaining overall title and footer parameters.
    title_text_on_off = par_dict["Overall title text on/off**"]. \
                                 replace(" ","").lower()
    footer_text_on_off = par_dict["Footer text on/off**"]. \
                                  replace(" ","").lower()
    
    # Initial checks of Overall title entries from parameter file
    if title_text_on_off not in ["on", "off"] and  \
        pd.isnull(title_text_on_off) == False:
        print("\nTitle text on/off in Parameter file has an incorrect entry. "
              "Entry needs to be either 'on' or 'off'.")
        sys.exit()              
        
    if title_text_on_off == "on":
        dict_title_values = {k: v for k, v in par_dict.items() \
                             if "Overall title" in str(k)} 
        
        for k,v in dict_title_values.items():
            if pd.isnull(v) == True:
                print(f"\nEntry for {k} in Parameter file is missing or "
                      "incorrect.")
                sys.exit()
        
        try:
            title_text_gap = float(par_dict["Overall title gap"])
        except:
            print("\nProblem with Overall title gap entry in Parameter file. "
                  "Check it is numeric.")
            sys.exit()
                
        try:
            title_text = par_dict["Overall title text"]
        except:
            print("\nProblem with Overall title text entry. Check it is a "
                  "string.")
            
        try:
            title_text_colour = float(par_dict["Overall title text colour"] \
                                     .replace(" ",""))
        except:
            print("\nProblem with Overall title text colour entry in "
                  "Parameter file. Check entry is numeric.")
            sys.exit()
            
        if title_text_colour < 1 or title_text_colour > col_max:
            print("\nOverall title text colour entry in Parameter file is"
                  " out of bounds or incorrect. See manual for range of"
                  " colour codes. These are presently 1-23.")
            sys.exit()
            
        try:
            title_text_bold = par_dict["Overall title text bold on/off"]. \
                                  replace(" ","").lower()
        except:
            print("\nProblem with Overall title text entry. Check it is a "
                  "string.")
            sys.exit()
                                  
        if title_text_bold not in ["on", "off"]:
            print("\nOverall title text bold on/off in Parameter file"
                  " needs to be either 'on' or 'off'.")
            sys.exit()
            
        try:
            title_font_size = float(par_dict["Overall title font size"]. \
                                    replace(" ",""))
            title_rotation = float(par_dict["Overall title rotation"]. \
                                   replace(" ",""))
        except:
            print("\nProblem with Overall title position entry / entries in "
                  "Parameter file. Check these are numeric.")
            sys.exit()          
        
        if title_rotation < 0 or title_rotation > 360:
            print("\nOverall title rotation in Parameter file is out of "
                  "bounds or incorrect.")
            sys.exit()
    
        try:
            title_y_pos = float(par_dict["Overall title Y position"]. \
                                replace(" ",""))
            title_x_pos = float(par_dict["Overall title X position"]. \
                                    replace(" ",""))
        except:
            print("\nProblem with Overall title position entry / entries in "
                  "Parameter file. Check these are numeric.")
            sys.exit()  
              
    # Initial checks of footer entries from Parameter file
    if footer_text_on_off not in ["on", "off"] and \
        pd.isnull(footer_text_on_off) == False:
        print("\nTitle text on/off has an incorrect entry. Enter 'off' if not"
              " required. Entry should be either 'on' or 'off'.")
        sys.exit()              
        
    if footer_text_on_off == "on":
        dict_footer_values = {k: v for k, v in par_dict.items() \
                              if "Footer" in str(k)} 
        
        for k,v in dict_footer_values.items():
            if pd.isnull(v) == True:
                print(f"\nEntry for {k} in Parameter file is missing or "
                      " incorrect.")
                sys.exit()
    
        try:
            footer_text = par_dict["Footer text"]
        except:
            print("\nProblem with Footer text entry Check it is a string.")
            sys.exit()
            
        try:
            footer_text_colour = float(par_dict["Footer text colour"] \
                                   .replace(" ",""))
        except:
            print("\nProblem with Footer text colour entry in Parameter file."
                  " Check entry is numeric.")
            sys.exit()          
        
        if footer_text_colour < 1 or footer_text_colour > col_max:
            print("\nOverall footer text colour entry in Parameter file "
                  "is out of bounds or incorrect. See manual for range of "
                  "colour codes. These are presently 1-23.")
            sys.exit()
    
        try:
            footer_text_bold = par_dict["Footer text bold on/off"] \
                                       .replace(" ","").lower()
        except:
            print("\nProblem with Overall title text entry. Check it is a "
                  "string.")
            sys.exit()
                                    
        if footer_text_bold not in ["on", "off"]:
            print("\nOverall footer text bold on/off in Parameter file needs"
                  " to be either 'on' or 'off'.")
            sys.exit() 
                                   
        try:                                                                
            footer_font_size = float(par_dict["Footer font size"] \
                                     .replace(" ",""))
            footer_rotation = float(par_dict["Footer rotation"] \
                                    .replace(" ",""))
        except:
            print("\nProblem with footer font size or rotation entries in "
                  "Parameter file. Check these are numeric.")
            sys.exit() 
            
        if footer_rotation < 0 or footer_rotation > 360:
            print("n\Overall footer rotation is out of bounds or incorrect.")
            sys.exit()
            
        try:
            footer_y_pos = float(par_dict["Footer Y position"] \
                                 .replace(" ",""))
            footer_x_pos = float(par_dict["Footer X position"] \
                                 .replace(" ",""))
        except:
            print("\nProblem with Footer position entry / entries in "
                  "Parameter file. Check these are numeric.")
            sys.exit()         
        
    # Obtaining X and Y title parameters and checks. Null values been checked 
    # earlier.
    try:
        x_title = par_dict["X title text**"]
    except:
        print("\nProblem with X title text entry. Check it is a string.")
        sys.exit()
    
    try:    
        y_title_rotation = float(par_dict["Y title rotation**"] \
                                 .replace(" ",""))
        x_title_rotation = float(par_dict["X title rotation**"] \
                                 .replace(" ",""))
        x_title_fontsize  = float(par_dict["X title font size**"] \
                                  .replace(" ",""))
        y_title_fontsize = float(par_dict["Y title font size**"] \
                                 .replace(" ",""))
        x_title_text_colour = float(par_dict["X title text colour**"] \
                                   .replace(" ",""))
    except:
        print("\nProblem with X or Y title numeric entries. Check entries are"
              " numeric.")
        sys.exit()  
    
    x_y_title_rotation_check = [y_title_rotation, x_title_rotation]
    
    if any(i < 0 or i > 360 for i in x_y_title_rotation_check) == True:
        print("\nCheck Y title rotation or X title rotation entries in "
              "Parameter file as they are out of range (0 to 360 degrees).")
        sys.exit()
    
    if x_title_text_colour < 0 or x_title_text_colour > col_max:
        print("\nX title text colour is out of range. See manual for range of"
              " colour codes. Presently these are from 1-23.")
        sys.exit()
        
    try:    
        x_title_text_bold = par_dict["X title bold on/off**"].replace(" ","") \
                                    .lower()
    except:
        print("\nProblem with X title bold on/off entry. Check entry is a "
              "string.")
        sys.exit()
    
    if x_title_text_bold not in ["on", "off"]:
        print("\nX title bold on/off entry in Parameter file needs to be"
              " either 'on' or 'off'.")
        sys.exit()
    
    ###########################################################################
    ###########################################################################
    # Obtain X and Y tick label parameters and check. Null values been checked 
    # earlier.
    try:
        x_lab_font = float(par_dict["X label font size**"].replace(" ",""))
        y_lab_font = float(par_dict["Y label font size**"].replace(" ",""))
        x_lab_colour = float(par_dict["X label colour**"].replace(" ",""))
        x_lab_rot = float(par_dict["X label rotation**"].replace(" ",""))
        y_lab_rot = float(par_dict["Y label rotation**"].replace(" ",""))
        y_lab_gap = float(par_dict["Y label gap**"].replace(" ",""))
    except:
        print("\nProblem with numeric entry for X or Y labels. Check entries "
              " for X label font size, Y label font size, X label colour, X "
              "label rotation, Y label rotation and Y label gap are numeric.")
        sys.exit()
    
    x_y_lab_rot = [x_lab_rot, y_lab_rot]    
    
    if any(i >360 or i < 0 for i in x_y_lab_rot) == True:
        print("\nX label rotation or Y label rotation are out of bounds of 0"
              " to 360 degrees range. Check numbers and formats.")
        sys.exit()
        
    ###########################################################################
    ###########################################################################
    # Odd scaling taxa. Find what the user wants to use as non_std_scaling
    # and get associated parameters and check. Can be up to 5 non_std_scaling
    # graphs at present. Could be expanded in the future but doubt would be
    # required.
    non_std_list = [non_std_scaling_1, non_std_scaling_2, non_std_scaling_3,\
                     non_std_scaling_4, non_std_scaling_5]
    non_std_list = ["none" if x == "NONE" else x for x in non_std_list]
    
    non_std_list_num = ["NSC_1", "NSC_2", "NSC_3", "NSC_4", "NSC_5"]
    
    nsc_diff = {x: y for x, y in zip(non_std_list_num, non_std_list)}
    
    # User input error checking for NSC values.
    for value, key in zip(nsc_diff.values(), nsc_diff.keys()):
        if value == "nan" or len(value) == 0:
            print("")
            print(f"\nFill {key} entries in Parameter file with 'none' if not"
                  " being used.")
            sys.exit()
            
        if any(value in w for w in data_list) != True and value != "none":
            print("")
            print(f"\nThe nominated NSC ({value}) in Parameter file is not "
                  "called any of the available element names or is mispelt.")
            sys.exit()
    
    # If any of the 5 non standard scaling options are selected load in the 
    # parameters required need to alter diff_list_ratios so are correctly
    # scaled based on user choices.
    if non_std_list[4] != "none" :
        if pd.isnull(non_std_list[4]) == False:
            diff_list_ratios_dict[non_std_scaling_5] = 1
            diff_list_ratios_dict[non_std_scaling_4] = 1
            diff_list_ratios_dict[non_std_scaling_3] = 1
            diff_list_ratios_dict[non_std_scaling_2] = 1
            diff_list_ratios_dict[non_std_scaling_1] = 1
    
    if non_std_list[3] != "none" and non_std_list[4] == "none":
        if pd.isnull(non_std_list[4]) == False and \
            pd.isnull(non_std_list[3]) == False:
            diff_list_ratios_dict[non_std_scaling_4] = 1
            diff_list_ratios_dict[non_std_scaling_3] = 1
            diff_list_ratios_dict[non_std_scaling_2] = 1
            diff_list_ratios_dict[non_std_scaling_1] = 1
        
        for x in range(ST, EN - 1):
            diff_list_ratios_dict[x] = diff_list_ratios_dict_1
    
    if non_std_list[2] != "none" and non_std_list[3] == "none":
        if pd.isnull(non_std_list[2]) == False and \
            pd.isnull(non_std_list[3]) == False:
            diff_list_ratios_dict[non_std_scaling_3] = 1
            diff_list_ratios_dict[non_std_scaling_2] = 1
            diff_list_ratios_dict[non_std_scaling_1] = 1
        
    if non_std_list[1] != "none" and non_std_list[2] == "none":
        if pd.isnull(non_std_list[1]) == False and \
            pd.isnull(non_std_list[2]) == False:
            diff_list_ratios_dict[non_std_scaling_2] = 1
            diff_list_ratios_dict[non_std_scaling_1] = 1
            
    if non_std_list[0] != "none" and non_std_list[1] == "none":
        if pd.isna(non_std_list[0]) == False and \
            pd.isna(non_std_list[1]) == False:
            diff_list_ratios_dict[non_std_scaling_1] = 1
    
    ###########################################################################
    # Get user options for NON_STD_SCALING 1 and check.
    non_std_spine_start_list = []
    
    if non_std_list[0] != "none":
        try:
            non_std_scaling_y_maj_int_1 = float(par_dict["NSC 1 y major tick " 
                                                         "interval"])
            non_std_scaling_y_min_int_1 = float(par_dict["NSC 1 y minor tick " 
                                                         "interval"])
            non_std_scaling_y_min_1 = float(par_dict["NSC 1 y min"])
            non_std_scaling_y_max_1 = float(par_dict["NSC 1 y max"])
            non_std_spine_on_off_1 = str(par_dict["NSC 1 spine on/off"]) \
                                                  .replace(" ","").lower()
            non_std_scaling_1_size = float(par_dict["NSC 1 size"] \
                                           .replace(" ",""))
            non_std_spine_start_1 = str(par_dict["NSC 1 spine start"]). \
                                                  replace(" ","")
            non_std_spine_start_list.append(non_std_spine_start_1)
        except:
            print("\nCheck NSC 1 y major tick interval, NSC 1 y minor tick "
                  "interval, NSC 1 y min, NSC 1 y max, NSC 1 spine on/off,"
                  " NSC 1 size or NSC spine start 1. A problem exists with"
                  " one of these entries. Check entry and format.")
            sys.exit()
            
        if non_std_spine_on_off_1 not in ["on","off"]:
            print("\nEntry for NSC 1 spine on/off must be either 'on' or" 
                  " 'off'. Check entry.")
            sys.exit()
            
        non_std_scaling_dict_1 = {k: v for k, v in par_dict.items() \
                          if "NSC 1" in str(k)}
        
        for k,v in non_std_scaling_dict_1.items():
            if pd.isnull(v) == True:
                print(f"\nEntry missing for {k} in Group 14 in Parameter"
                      " file.")
                sys.exit() 
            if k == "NSC 1 y minor tick interval" and v == str(0) and \
                     y_minor_ticks_on_off == "on":
                print("\nY minor ticks have been selected as on so zero is"
                      " not permitted as entry for NSC 1 y min. Choose"
                      " sensible number that is a division of the interval"
                      " stated in the NSC 1 y max entry.")
                sys.exit()
            if k == "NSC 1 spine start" and v not in ["mini","0"]:
                print("\nNSC spine start 1 entry in Parameter file must be "
                      "either 'mini' or '0'. Check for spaces in entry.")
                sys.exit()
                
        # Apply size choices from user to graph scaling
        diff_list_ratios_dict[non_std_scaling_1] = \
            diff_list_ratios_dict[non_std_scaling_1] \
            * (non_std_scaling_1_size)
    
    # User input error checking. Make sure the slots for NSC are used in order
    if non_std_list[1] !="none":
        if nsc_diff["NSC_1"] == "none":
            print("")
            print("\nUse earlier NSC slots before NSC 2 if they are listed as"
                  " none in Parameter file.")
            sys.exit()
    
    ###########################################################################
    # Get user options for NON_STD_SCALING 2 and check.
    if non_std_list[1] != "none":
        try:
            non_std_scaling_y_maj_int_2 = float(par_dict["NSC 2 y major tick " 
                                                         "interval"])
            non_std_scaling_y_min_int_2 = float(par_dict["NSC 2 y minor tick " 
                                                         "interval"])
            non_std_scaling_y_min_2 = float(par_dict["NSC 2 y min"])
            non_std_scaling_y_max_2 = float(par_dict["NSC 2 y max"])
            non_std_spine_on_off_2 = str(par_dict["NSC 2 spine on/off"]) \
                                                  .replace(" ","").lower()
            non_std_scaling_2_size = float(par_dict["NSC 2 size"] \
                                           .replace(" ",""))
            non_std_spine_start_2 = str(par_dict["NSC 2 spine start"]) \
                                                  .replace(" ","")
            non_std_spine_start_list.append(non_std_spine_start_2)
        except:
            print("\nCheck NSC 2 y major tick interval, NSC 2 y minor tick "
                  "interval, NSC 2 y min, NSC 2 y max NSC 2 spine on/off,"
                  " NSC 2 size or NSC spine start 2. A problem exists with"
                  " one of these entries. Check entry and format.")
            sys.exit()
            
        if non_std_spine_on_off_2 not in ["on","off"]:
            print("\nEntry for NSC 2 spine on/off must be either 'on'" 
                  " or 'off'. Check entry.")
            sys.exit()
            
        non_std_scaling_dict_2 = {k: v for k, v in par_dict.items() \
                          if "NSC 2" in str(k)}
        
        for k,v in non_std_scaling_dict_2.items():
            if pd.isnull(v) == True:
                print(f"\nEntry missing for {k} in Group 14 in Parameter "
                      "file.")
                sys.exit() 
            if k == "NSC 2 y minor tick interval" and v == str(0) and \
                     y_minor_ticks_on_off == "on":
                print("\nY minor ticks have been selected as on so zero is"
                      " not permitted as entry for NSC 2 y min. Choose"
                      " sensible number that is a division of the interval"
                      " stated in the NSC 2 y max entry.")
                sys.exit()
            if k == "NSC 2 spine start" and v not in ["mini","0"]:
                print("\nNSC spine start 2 entry in Parameter file must be "
                      "either 'mini' or '0'. Check for spaces in entry.")
                sys.exit()
    
        # Apply size choices from user to graph scaling.
        diff_list_ratios_dict[non_std_scaling_2] = \
            diff_list_ratios_dict[non_std_scaling_2] * (non_std_scaling_2_size)
        
    # User input error checking. Make sure the slots for NSC are used in order.
    if non_std_list[2] !="none":
        if nsc_diff["NSC_1"] == "none" or nsc_diff["NSC_2"] == "none":
            print("")
            print("\nUse earlier NSC slots before NSC 3 if they are listed as"
                  " none in Parameter file.")
            sys.exit()
            
    ###########################################################################
    # Get user options for NON_STD_SCALING 3 and check.
    if non_std_list[2] != "none":
        try:
            non_std_scaling_y_maj_int_3 = float(par_dict["NSC 3 y major tick " 
                                                         "interval"])
            non_std_scaling_y_min_int_3 = float(par_dict["NSC 3 y minor tick " 
                                                         "interval"])
            non_std_scaling_y_min_3 = float(par_dict["NSC 3 y min"])
            non_std_scaling_y_max_3 = float(par_dict["NSC 3 y max"])
            non_std_spine_on_off_3 = str(par_dict["NSC 3 spine on/off"]) \
                                                  .replace(" ","").lower()
            non_std_scaling_3_size = float(par_dict["NSC 3 size"] \
                                           .replace(" ",""))
            non_std_spine_start_3 = str(par_dict["NSC 3 spine start"]) \
                                                  .replace(" ","")
            non_std_spine_start_list.append(non_std_spine_start_3)
        except:
            print("\nCheck NSC 3 y major tick interval, NSC 3 y minor tick "
                  "interval, NSC 3 y min, NSC 3 y max NSC 3 spine on/off,"
                  " NSC 3 size or NSC spine start 3. A problem exists with"
                  " one of these entries. Check entry and format.")
            sys.exit()
            
        if non_std_spine_on_off_3 not in ["on","off"]:
            print("\nEntry for NSC 3 spine on/off must be either 'on' " 
                  "or 'off'. Check entry.")
            sys.exit()
            
        non_std_scaling_dict_3 = {k: v for k, v in par_dict.items() \
                          if "NSC 3" in str(k)}
        
        for k,v in non_std_scaling_dict_3.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k} in Group 14 in Parameter file.")
                sys.exit() 
            if k == "NSC 3 y minor tick interval" and v == str(0) and \
                     y_minor_ticks_on_off == "on":
                print("\nY minor ticks have been selected as on so zero is"
                      " not permitted as entry for NSC 3 y min. Choose"
                      " sensible number that is a division of the interval"
                      " stated in the NSC 3 y max entry.")
                sys.exit()
            if k == "NSC 3 spine start" and v not in ["mini","0"]:
                print("\nNSC spine start 3 entry in Parameter file must be "
                      "either 'mini' or '0'. Check for spaces in entry.")
                sys.exit()
    
        diff_list_ratios[3] = diff_list_ratios[3] * \
                              (non_std_scaling_3_size / 100)
        non_std_spine_start_list.append(non_std_spine_start_3)
        
        # Apply size choices from user to graph scaling.
        diff_list_ratios_dict[non_std_scaling_3] = \
            diff_list_ratios_dict[non_std_scaling_3] * (non_std_scaling_3_size)
        
    # User input error checking. Make sure the slots for NSC are used in order.
    if non_std_list[3] != "none":
        if nsc_diff["NSC_1"] == "none" or nsc_diff["NSC_2"] == "none" or \
            nsc_diff["NSC_3"] == "none":
            print("")        
            print("\nUse earlier NSC slots before NSC 4 if they are listed as"
                  " none in Parameter file.")
            sys.exit()
    
    ###########################################################################
    # Get user options for NON_STD_SCALING 4 and check.
    if non_std_list[3]!= "none":
        try:
            non_std_scaling_y_maj_int_4 = float(par_dict["NSC 4 y major tick " 
                                                         "interval"])
            non_std_scaling_y_min_int_4 = float(par_dict["NSC 4 y minor tick " 
                                                         "interval"])
            non_std_scaling_y_min_4 = float(par_dict["NSC 4 y min"])
            non_std_scaling_y_max_4 = float(par_dict["NSC 4 y max"])
            non_std_spine_on_off_4 = str(par_dict["NSC 4 spine on/off"]) \
                                                  .replace(" ","").lower()
            non_std_scaling_4_size = float(par_dict["NSC 4 size"] \
                                           .replace(" ",""))
            non_std_spine_start_4 = str(par_dict["NSC 4 spine start"]). \
                                                  replace(" ","")
            non_std_spine_start_list.append(non_std_spine_start_4)
        except:
            print("\nCheck NSC 4 y major tick interval, NSC 4 y minor tick "
                  "interval, NSC 4 y min, NSC 4 y max NSC 4 spine on/off,"
                  " NSC 4 size or NSC spine start 4. A problem exists with"
                  " one of these entries. Check entry and format.")
            sys.exit()
            
        if non_std_spine_on_off_4 not in ["on","off"]:
            print("\nEntry for NSC 4 spine on/off must be either 'on' or" 
                  " 'off'. Check entry.")
            sys.exit()
            
        non_std_scaling_dict_4 = {k: v for k, v in par_dict.items() \
                          if "NSC 4" in str(k)}
        
        for k,v in non_std_scaling_dict_4.items():
            if pd.isnull(v) == True:
                print(f"\nEntry missing for {k} in Group 14 in Parameter "
                      "file.")
                sys.exit() 
            if k == "NSC 4 y minor tick interval" and v == str(0) and \
                     y_minor_ticks_on_off == "on":
                print("\nY minor ticks have been selected as on so zero is"
                      " not permitted as entry for NSC 4 y min. Choose"
                      " sensible number that is a division of the interval"
                      " stated in the NSC 4 y max entry.")
                sys.exit()
            if k == "NSC 4 spine start" and v not in ["mini","0"]:
                print("\nNSC spine start 4 entry in Parameter file must be "
                      "either 'mini' or '0'. Check for spaces in entry.")
                sys.exit()
        
        # Apply size choices from user to graph scaling.
        diff_list_ratios_dict[non_std_scaling_4] = \
            diff_list_ratios_dict[non_std_scaling_3] * (non_std_scaling_4_size)
            
    # User input error checking. Make sure the slots for NSC are used in order.
    if non_std_list[4] != "none": 
        if nsc_diff["NSC_1"] == "none" or nsc_diff["NSC_2"] == "none" or \
            nsc_diff["NSC_3"] == "none" or nsc_diff["NSC_4"] == "none":
            print("")        
            print("\nUse earlier NSC slots before NSC 5 if they are listed as"
                  " none in Parameter file.")
            sys.exit()
            
    ###########################################################################
    # Get user options for NON_STD_SCALING 5 and check.
    if non_std_list[4] != "none":
        try:
            non_std_scaling_y_maj_int_5 = float(par_dict["NSC 5 y major tick " 
                                                         "interval"])
            non_std_scaling_y_min_int_5 = float(par_dict["NSC 5 y minor tick " 
                                                         "interval"])
            non_std_scaling_y_min_5 = float(par_dict["NSC 5 y min"])
            non_std_scaling_y_max_5 = float(par_dict["NSC 5 y max"])
            non_std_spine_on_off_5 = str(par_dict["NSC 5 spine on/off"]). \
                                                  replace(" ","").lower()
            non_std_scaling_5_size = float(par_dict["NSC 5 size"] \
                                           .replace(" ",""))
            non_std_spine_start_5 = str(par_dict["NSC 5 spine start"]) \
                                                  .replace(" ","")
            non_std_spine_start_list.append(non_std_spine_start_5)
        except:
            print("\nCheck NSC 5 y major tick interval, NSC 5 y minor tick "
                  "interval, NSC 5 y min, NSC 5 y max NSC 5 spine on/off,"
                  " NSC 5 size or NSC spine start 5. A problem exists with"
                  " one of these entries. Check entry and format.")
            sys.exit()
            
        if non_std_spine_on_off_5 not in ["on","off"]:
            print("\nEntry for NSC 5 spine on/off must be either 'on' or" 
                  " 'off'. Check entry.")
            sys.exit()
            
        non_std_scaling_dict_5 = {k: v for k, v in par_dict.items() \
                          if "NSC 5" in str(k)}
        
        for k,v in non_std_scaling_dict_5.items():
            if pd.isnull(v) == True:
                print(f"\nEntry missing for {k} in Group 14 in Parameter "
                      "file.")
                sys.exit() 
            if k == "NSC 5 y minor tick interval" and v == str(0) and \
                     y_minor_ticks_on_off == "on":
                print("\nY minor ticks have been selected as on so zero is"
                      " not permitted as entry for NSC 5 y min. Choose"
                      " sensible number that is a division of the interval"
                      " stated in the NSC 5 y max entry.")
                sys.exit()
            if k == "NSC 5 spine start" and v not in ["mini","0"]:
                print("\nNSC spine start 5 entry in Parameter file must be "
                      "either 'mini' or '0'. Check for spaces in entry. ")
                sys.exit()
       
        # Apply size choices from user to graph scaling.
        diff_list_ratios_dict[non_std_scaling_5] = \
            diff_list_ratios_dict[non_std_scaling_5] * (non_std_scaling_5_size)
    
    ###########################################################################
    # Non standard spine starts at either 0 or the min of data.
    non_std_spine_start_list = [x.lower() if x != 0 else x for x in \
                                non_std_spine_start_list]
    
    ###########################################################################
    ###########################################################################
    # RC ages if supplied. Bring in all required parameters and check what
    # user has entered in Parameter file.
    rc_ages_on_off = par_dict["RC ages on/off**"].replace(" ","").lower()
    
    # Check entry is provided.
    rc_check_list = ["on", "off"]
    
    if rc_ages_on_off not in rc_check_list:
        print("\nIncorrect entry for RC ages on/off. If not using feature "
              "provide an entry of 'off' in Parameter file. Entry needs to be"
              " either 'on' or 'off'.")
        sys.exit()         
    
    # Check RC entries
    if rc_ages_on_off == "on":
    
        rc_age_title_on_off = par_dict["RC age title on/off"]
        
        if pd.isnull(rc_age_title_on_off) == True:
            print("\nEntry for RC age title on/off is required. Entry should"
                  " be 'on' or off'.")
            sys.exit()
            
        try:    
            rc_age_depths = par_dict["RC age depth label positions"] \
                             .replace(" ","").split(",")
            rc_age_depths = [float(x) for x in rc_age_depths]
        except:
            print("\nEntries for RC age depth label positions are required.")
            sys.exit() 
            
        try:
            rc_age_location_offset = float(par_dict \
                                           ["RC age label position "
                                            "offset"].replace(" ",""))
            if pd.isnull(rc_age_location_offset) == True:
                print("\nEntry for RC age label position offset in Parameter "
                      "file is required.")
                sys.exit()
        except:
            print("\nEntry for RC age label position offset in Parameter"
                  " file is required.")              
            sys.exit()        
            
        try:
            rc_age_labels = par_dict["RC age labels"].split(",")
        except:
            print("\nProblem with RC age labels. Check entries for these in "
                  "Parameter file.")
            sys.exit()        
            
        try:
            rc_age_labels_font_size = float(par_dict["RC age label font "
                                            "size"].replace(" ",""))
            rc_age_labels_colour = float(par_dict["RC age labels colour"] \
                                      .replace(" ",""))
            rc_age_labels_bold = par_dict["RC age labels bold on/off"] \
                                      .replace(" ","").lower()
            rc_age_labels_rotation = float(par_dict["RC age labels "
                                            "rotation"].replace(" ",""))
        except:
            print("\nProblem with one of the entries in Parameter file for "
                  "either RC age label font size, RC age labels colour,"
                  " RC age labels bold on/off or RC age labels rotation"
                  " entries. Check formats are correct.")
            sys.exit()
            
        par_dict_rc_labels_values = {k: v for k, v in par_dict.items() \
                      if "RC age labels" in str(k)} 
    
        for k,v in par_dict_rc_labels_values.items():
            if pd.isnull(v) == True:
                print(f" \nEntry missing for {k}.")
                sys.exit()                      
        
        if rc_age_labels_bold not in ["on", "off"]:
            print("\nEntry for RC age labels bold on/off in Parameter file is"
                  " required. Enter 'on' or 'off'.")
            sys.exit()            
            
        if rc_age_labels_rotation < 0 or rc_age_labels_rotation > 360:
            print("\nEntry for RC age labels rotation in Parameter file is"
                  " not between 0 and 360.")
            sys.exit()                 
    
        # User input error checking for length of list of labels and ages.
        # Must be the same length.
        if len(rc_age_labels) != len(rc_age_depths):
            print("")
            print("\nError in RC label depths in Parameter file. Unequal"
                  " number of depths and labels.")
            sys.exit()
    
    # Load in data for RC age title if it is specified as being 'on' and check.
        if rc_age_title_on_off == "on":
            rc_age_title = par_dict["RC age title"]
    
            try:
                rc_age_title_depth = float(par_dict["RC age title depth "
                                          "position"].replace(" ",""))
                rc_age_title_offset = float(par_dict["RC age title offset "
                                            "position"].replace(" ",""))
                rc_age_title_font_size = float(par_dict["RC age title font "
                                              "size"].replace(" ",""))
                rc_age_title_colour = float(par_dict["RC age title colour"]. \
                                            replace(" ",""))
                rc_age_title_bold = par_dict["RC age title bold on/off"]. \
                                            replace(" ","").lower()
                rc_age_title_rotation = float(par_dict["RC age title rotation"]. \
                                              replace(" ",""))
            except:
                print("\nProblem with one of the entries in Parameter file"
                      " for either RC age title depth position, RC age title"
                      " offset position, RC age title font size, RC age title"
                      " colour, RC age title bold on/off or RC age title"
                      " rotation entries.Check formats are correct.")
                sys.exit()
                
            par_dict_RC_title_values = {k: v for k, v in par_dict.items() \
                          if "RC age title" in str(k)} 
        
            for k,v in par_dict_RC_title_values.items():
                if pd.isnull(v) == True:
                    print(f" \n Entry missing for {k}.")
                    sys.exit()            
            
            if rc_age_title_colour < 0 or rc_age_title_colour > col_max:
                print("\nEntry for RC age title colour in Parameter file is"
                      " out of bounds.")
                sys.exit()
                
            if rc_age_title_bold not in ["on", "off"]:
                print("\nEntry for RC age title bold on/off in Parameter file"
                      " is required. Enter 'on' or 'off'.")
                sys.exit()            
                
            if rc_age_title_rotation < 0 or rc_age_title_rotation > 360:
                print("\nEntry for RC age title rotation in Parameter file is"
                      " not between 0 and 360.")
                sys.exit()
    
    ###########################################################################
    ###########################################################################
    # Date line ages if supplied bring in all required parameters from
    # Parameter file and check.
    int_ages_on_off = par_dict["INT ages on/off**"].replace(" ","").lower()
    
    # Check entry is provided.
    if int_ages_on_off not in ["on", "off"]:
        print("\nIncorrect entry for INT ages on or off in Parameter file. If"
              " not using feature provide an entry of 'off' in Parameter"
              " file. Entries should be 'on' or 'off'.")
        sys.exit()
    
    # Obtain INT parameters from Parameter file and check entries.
    if int_ages_on_off == "on":
        
        int_age_title_on_off = str(par_dict["INT age title on/off"]). \
                               replace(" ",""). lower()
                               
        if int_age_title_on_off not in ["on","off"]:
            print("\nINT age title on/off entry should be either 'on' or"
                  " 'off'.")
            sys.exit()
        
        try:
            int_age_depths = par_dict["INT age depth labels positions"] \
                                     .replace(" ","").split(",")
            int_age_depths = [float(x) for x in int_age_depths]
        except:
            print("\nCheck entries and formats for INT age depth labels "
                  "positions.")
            sys.exit()
        
        if any(pd.isnull(int_age_depths)):
            print("\nEntries for INT age depth labels positions in Parameter "
                  "file required.")
            sys.exit()
        
        try:
            int_age_location_offset = float(par_dict \
                                            ["INT age labels position offset"] \
                                                .replace(" ",""))
        except:
            print("\nCheck entry and format for INT age labels position"
                  " offset in Parameter file.")
            sys.exit()        
            
        if pd.isnull(int_age_location_offset) == True:
            print("\nEntry for INT age labels position offset in Parameter"
                  " file is required.")
            sys.exit()
        
        try:
            int_age_labels = par_dict["INT age labels"].replace(" ","") \
                                                       .split(",")
        except:
            print("\nCheck Entry for INT age labels.")
            sys.exit()
    
        try:
            int_age_labels_font_size = float(par_dict["INT age labels font "
                                            "size"].replace(" ",""))
            int_age_labels_colour = float(par_dict["INT age labels colour"]. \
                                          replace(" ",""))
            int_age_labels_bold = par_dict["INT age labels bold on/off"]. \
                                          replace(" ","").lower()
            int_age_labels_rotation = float(par_dict["INT age labels "
                                            "rotation"].replace(" ",""))
        except:
            print("\nProblem with entry for INT age labels font size, INT age"
                  " labels colour, INT age labels bold on/off, or INT age"
                  " labels rotation. Check entries and formats.")
            sys.exit()
                
        par_dict_int_labels_values = {k: v for k, v in par_dict.items() \
                      if "INT age labels" in str(k)} 
    
        for k,v in par_dict_int_labels_values.items():
            if pd.isnull(v) == True:
                print(f" \nEntry missing for {k} in Parameter file.")
                sys.exit()                      
        
        if int_age_labels_bold not in ["on", "off"]:
            print("\nEntry for INT age labels bold on/off in Parameter file"
                  " is required. Enter 'on' or 'off'.")
            sys.exit()            
            
        if int_age_labels_rotation < 0 or int_age_labels_rotation > 360:
            print("\nEntry for INT age labels rotation in Parameter file is"
                  " not between 0 and 360.")
            sys.exit()
                
        int_age_depth_labels = par_dict["INT age depth labels positions"]. \
                               replace(" ","").split(",")
            
        if any(pd.isnull(int_age_depth_labels)) == True:
            print("\nThere is a missing value or an empty space in the INT"
                  " age depth labels positions entry in Parameter file.")
            sys.exit()    
    
        if int_age_title_on_off == "on":
            int_age_title = par_dict["INT age title"]
            
            par_dict_INT_title_values = {k: v for k, v in par_dict.items() \
                          if "INT age title" in str(k)} 
        
            for k,v in par_dict_INT_title_values.items():
                if pd.isnull(v) == True:
                    print(f" \nEntry missing for {k} in Parameter file.")
                    sys.exit()
            try:
                int_age_title_depth = float(par_dict["INT age title depth "
                                           "position"].replace(" ",""))
                int_age_title_offset = float(par_dict["INT age title offset "
                                            "position"].replace(" ",""))
                int_age_title_font_size = float(par_dict["INT age title font "
                                                "size"].replace(" ",""))
                int_age_title_colour = float(par_dict["INT age title colour"] \
                                            .replace(" ","")) 
            except:
                print("\nProblem with INT age title depth position, INT age "
                      "title offset position, INT age title font size or INT"
                      " age title colour entry. Check these entries and their "
                      " format.")
                sys.exit()
                
            if int_age_title_colour < 0 or int_age_title_colour > col_max:
                print("\nEntry for INT age title colour in Parameter file is"
                      " out of range.")
                sys.exit()
                
            int_age_title_bold = par_dict["INT age title bold on/off"] \
                                     .replace(" ","").lower()
                                     
            if int_age_title_bold not in ["on", "off"]:
                print("\nEntry for INT age title bold on/off in Parameter"
                      " file required to be 'on' or 'off'.")
                sys.exit()
                
            int_age_title_rotation = float(par_dict["INT age title "
                                          "rotation"].replace(" ",""))
                
            if int_age_title_rotation < 0 or int_age_title_rotation > 360:
                print("\nEntry for INT age title rotation in Parameter file "
                      "must be between 0 and 360.")
                sys.exit()
            
        
        par_dict_int_lines_values = {k: v for k, v in par_dict.items() \
                          if "INT lines" in str(k)}
    
        try:
            int_lines_colour = float(par_dict["INT lines colour"] \
                                     .replace(" ",""))
            int_lines_offset = float(par_dict["INT lines offset"] \
                                     .replace(" ",""))
            int_lines_width = float(par_dict["INT lines width"] \
                                    .replace(" ",""))
            int_lines_depth_length = float(par_dict["INT lines depth length"] \
                                         .replace(" ","")) 
            int_lines_corr = float(par_dict["INT lines width correction"] \
                                  .replace(" ",""))  
            int_lines_corr_l = float(par_dict["INT lines length correction"] \
                                    .replace(" ",""))
        except:
            print("\nCheck entries for INT lines colour, INT lines offset INT"
                  " lines width, INT lines depth length, INT lines width "
                  "correction and INT lines length correction. One of these "
                  "entries is erroneous. Check entries and formats.")
            sys.exit()             
            
        for k,v in par_dict_int_lines_values.items():
            if pd.isnull(v) == True:
                    print(f" \n Entry missing for {k}")
                    sys.exit()
                    
        if int_lines_colour < 0 or int_lines_colour > col_max:
            print("\nEntry for INT lines colour in Parameter file is out of "
                  "range.")
            sys.exit()
    
        try:
            int_umd_age = int(par_dict["INT upper most depth age"]. \
                                replace(" ",""))
        except:
            print("\nEntry for INT upper most depth age is required. Check "
                  "entry and format.")
            sys.exit()
        
        if pd.isnull(int_umd_age) == True:
            print("\nEntry missing for INT upper most depth age in Parameter "
                  "file.")
            sys.exit()
            
        # User input error checking.Labels and depths need to have same length
        if len(int_age_labels) != len(int_age_depths):
            print("")
            print("\nError in INT label depths in Parameter file. Unequal "
                  "number of depths and labels.")
            sys.exit()
    
    ###########################################################################
    ###########################################################################
    # Grouping annotation data 1-10. Bring in required parameters from 
    # Parameter file for any grouping annotations required for possible
    # groups 1-10 and  check.
    try:
        group_anno_1 = str(par_dict["Grouping annotation 1 on/off**"]). \
                               replace(" ","").lower()
        group_anno_2 = str(par_dict["Grouping annotation 2 on/off**"]). \
                               replace(" ","").lower()
        group_anno_3 = str(par_dict["Grouping annotation 3 on/off**"]). \
                               replace(" ","").lower()
        group_anno_4 = str(par_dict["Grouping annotation 4 on/off**"]). \
                               replace(" ","").lower()
        group_anno_5 = str(par_dict["Grouping annotation 5 on/off**"]). \
                               replace(" ","").lower()
        group_anno_6 = str(par_dict["Grouping annotation 6 on/off**"]). \
                               replace(" ","").lower()
        group_anno_7 = str(par_dict["Grouping annotation 7 on/off**"]). \
                               replace(" ","").lower()
        group_anno_8 = str(par_dict["Grouping annotation 8 on/off**"]). \
                               replace(" ","").lower()
        group_anno_9 = str(par_dict["Grouping annotation 9 on/off**"]). \
                               replace(" ","").lower()
        group_anno_10 = str(par_dict["Grouping annotation *10 on/off**"]). \
                                replace(" ","").lower()
    except:
        print("\nGrouping annotation on/off entries must be filled in with "
              "either 'on' or 'off'. Check all 10 entries Grouping annotation"
              " on/off 1-10 and eneter either 'on' or 'off'.")
        sys.exit()
    
    # Create various empy lists to be used subsequently for groupings.
    group_list = []
    group_lw = []
    group_corr =[ ]
    group_corr_line = []
    
    ###########################################################################
    # Group 1 annotation.
    if group_anno_1 == "on":
        # Create dictionary of grouping entries
        par_dict_G1_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 1" in str(k)} 
        
        # Check for missing entries
        for k,v in par_dict_G1_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
        # Check entries are provided
        try:
            group_anno_1_start = str(par_dict["Grouping annotation 1 start"]) \
                                    .strip()
            group_anno_1_title = str(par_dict["Grouping annotation 1 title"]) \
                                    .strip()
            group_anno_1_title_bold = str(par_dict["Grouping annotation 1 "
                                         "title bold on/off"]).replace(" ","") \
                                          .lower()
        except:
            print("\nCheck entries for Grouping annotation 1 start, Grouping "
                  "annotation 1 title and Grouping annotation 1 title bold "
                  "on/off. One of these is erroneous. Check entry and format.")
            sys.exit()
        
        # Check entries
        try:
            group_anno_1_title_colour = float(par_dict["Grouping annotation 1 "
                                                       "title colour"])
            group_anno_1_title_font_size = float(par_dict["Grouping annotation"
                                                          " 1 title font size"])    
            group_anno_1_line_colour = float(par_dict["Grouping annotation 1 "
                                                      "line colour"])
            group_anno_1_line_width = float(par_dict["Grouping annotation 1 "
                                                     "line width"])    
            group_anno_1_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 1 "
                                                    "line start x"])
            group_anno_1_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 1 "
                                                              "line start y"])
            group_anno_1_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 1 line end x"])
            group_anno_1_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "1 line end y"])
            group_anno_1_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 1 "
                                                         "tag end x"])
            group_anno_1_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 1 "
                                                         "tag end y"])
            group_anno_1_corr = float(par_dict["Grouping annotation 1 tag "
                                               "correction"])
            group_anno_1_line_y_correction = float(par_dict["Grouping "
                                                            "annotation 1 line"
                                                            " correction"])
        except:
            print("\nCheck entries for Group 1 annotation in Parameter file."
                  " One of the numeric entries is missing or erroneous. Check"
                  " entries and formats.")
            sys.exit()
        
        group_list.append("G1")
        group_lw.append(group_anno_1_line_width)
        group_corr.append(group_anno_1_corr)
        group_corr_line.append(group_anno_1_line_y_correction)
    
        # Further entry error checks
        if group_anno_1_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 1 title bold on/off "
                  "in Parameter file is required. Entry should be either 'on'"
                  " or 'off'.")
            sys.exit()
            
        if group_anno_1_title_colour < 0 or group_anno_1_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 1 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_1_line_colour < 0 or group_anno_1_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 1 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 2 annotation.
    if group_anno_2 == "on":
        
        # Create dictionary of group entries
        par_dict_G2_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 2" in str(k)} 
            
        # Check entries exist
        for k,v in par_dict_G2_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
       # Check grouping entries
        try:
            group_anno_2_start = str(par_dict["Grouping annotation 2 start"]) \
                                    .strip()
            group_anno_2_title = str(par_dict["Grouping annotation 2 title"]) \
                                    .strip()
            group_anno_2_title_bold = str(par_dict["Grouping annotation 2 "
                                         "title bold on/off"]) \
                                          .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 2 start, "
                  "Grouping annotation 2 title and Grouping annotation 2"
                  " title bold on/off. One of these is erroneous. Check"
                  " entry and format.")
            sys.exit()
        
        try:
            group_anno_2_title_colour = float(par_dict["Grouping annotation 2 "
                                                       "title colour"])
            group_anno_2_title_font_size = float(par_dict["Grouping "
                                                          "annotation 2 "
                                                          "title font size"])    
            group_anno_2_line_colour = float(par_dict["Grouping annotation 2 "
                                                      "line colour"])
            group_anno_2_line_width = float(par_dict["Grouping annotation 2 "
                                                     "line width"])    
            group_anno_2_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 2 "
                                                    "line start x"])
            group_anno_2_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 2 "
                                                              "line start y"])
            group_anno_2_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 2 line end x"])
            group_anno_2_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "2 line end y"])
            group_anno_2_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 2 "
                                                         "tag end x"])
            group_anno_2_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 2 "
                                                         "tag end y"])
            group_anno_2_corr = float(par_dict["Grouping annotation 2 tag "
                                               "correction"])
            group_anno_2_line_y_correction = float(par_dict["Grouping "
                                                            "annotation 2 line"
                                                            " correction"])
        except:
            print("\nCheck entries for Group 2 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G2")
        group_lw.append(group_anno_2_line_width)
        group_corr.append(group_anno_2_corr)
        group_corr_line.append(group_anno_2_line_y_correction)
        
        # Futher entry checks
        if group_anno_2_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 2 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or"
                  " 'off'.")
            sys.exit()
            
        if group_anno_2_title_colour < 0 or group_anno_2_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 2 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_2_line_colour < 0 or group_anno_2_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 2 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 3 annotation.
    if group_anno_3 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G3_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 3" in str(k)} 
        
        # Check entries exist
        for k,v in par_dict_G3_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
       # Error checks on grouping entries
        try:
            group_anno_3_start = str(par_dict["Grouping annotation 3 start"]) \
                                    .strip()
            group_anno_3_title = str(par_dict["Grouping annotation 3 title"]) \
                                    .strip()
            group_anno_3_title_bold = str(par_dict["Grouping annotation 3 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 3 start, Grouping "
                  "annotation 3 title and Grouping annotation 3 title bold "
                  "on/off. One of these is erroneous. Check entry and format.")
            sys.exit()
        
        try:
            group_anno_3_title_colour = float(par_dict["Grouping annotation 3 "
                                                       "title colour"])
            group_anno_3_title_font_size = float(par_dict["Grouping "
                                                          "annotation 3 "
                                                          "title font size"])    
            group_anno_3_line_colour = float(par_dict["Grouping annotation 3 "
                                                      "line colour"])
            group_anno_3_line_width = float(par_dict["Grouping annotation 3 "
                                                     "line width"])    
            group_anno_3_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 3 "
                                                    "line start x"])
            group_anno_3_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 3 "
                                                              "line start y"])
            group_anno_3_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 3 line end x"])
            group_anno_3_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "3 line end y"])
            group_anno_3_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 3 "
                                                         "tag end x"])
            group_anno_3_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 3 "
                                                         "tag end y"])
            group_anno_3_corr = float(par_dict["Grouping annotation 3 tag "
                                               "correction"])
            group_anno_3_line_y_correction = float(par_dict["Grouping "
                                                            "annotation 3 "
                                                            "line correction"])
        except:
            print("\nCheck entries for Group 3 annotation in Parameter file."
                  " One of the numeric entries is missing or erroneous."
                  " Check entries and formats.")
            sys.exit()
        
        group_list.append("G3")
        group_lw.append(group_anno_3_line_width)
        group_corr.append(group_anno_3_corr)
        group_corr_line.append(group_anno_3_line_y_correction)
    
        # Further grouping entry error checks
        if group_anno_3_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 3 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' "
                  "or 'off'.")
            sys.exit()
            
        if group_anno_3_title_colour < 0 or group_anno_3_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 3 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_3_line_colour < 0 or group_anno_3_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 3 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 4  annotation.
    if group_anno_4 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G4_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 4" in str(k)} 
        
        # Check entries exist
        for k,v in par_dict_G4_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
       
        # Error check entries for grouping
        try:
            group_anno_4_start = str(par_dict["Grouping annotation 4 start"]) \
                                    .strip()
            group_anno_4_title = str(par_dict["Grouping annotation 4 title"]) \
                                    .strip()
            group_anno_4_title_bold = str(par_dict["Grouping annotation 4 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 4 start, "
                  "Grouping annotation 4 title and Grouping annotation 4 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_4_title_colour = float(par_dict["Grouping annotation 4 "
                                                       "title colour"])
            group_anno_4_title_font_size = float(par_dict["Grouping "
                                                          "annotation 4 "
                                                          "title font size"])    
            group_anno_4_line_colour = float(par_dict["Grouping annotation 4 "
                                                      "line colour"])
            group_anno_4_line_width = float(par_dict["Grouping annotation 4 "
                                                     "line width"])    
            group_anno_4_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 4 "
                                                    "line start x"])
            group_anno_4_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 4 "
                                                              "line start y"])
            group_anno_4_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 4 line end x"])
            group_anno_4_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "4 line end y"])
            group_anno_4_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 4 "
                                                         "tag end x"])
            group_anno_4_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 4 "
                                                         "tag end y"])
            group_anno_4_corr = float(par_dict["Grouping annotation 4 tag "
                                               "correction"])
            group_anno_4_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 4 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 4 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G4")
        group_lw.append(group_anno_4_line_width)
        group_corr.append(group_anno_4_corr)
        group_corr_line.append(group_anno_4_line_y_correction)
    
        # Further error checks on grouping entries
        if group_anno_4_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 4 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or"
                  " 'off'.")
            sys.exit()
            
        if group_anno_4_title_colour < 0 or group_anno_4_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 4 title colour in "
                  " colour Parameter file is out of bounds. Refer to manual"
                  " forcodes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_4_line_colour < 0 or group_anno_4_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 4 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 5 annotation.
    if group_anno_5 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G5_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 5" in str(k)} 
        
        # Check entries exist
        for k,v in par_dict_G5_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
        # Error check grouping entries
        try:
            group_anno_5_start = str(par_dict["Grouping annotation 5 start"]) \
                                    .strip()
            group_anno_5_title = str(par_dict["Grouping annotation 5 title"]) \
                                    .strip()
            group_anno_5_title_bold = str(par_dict["Grouping annotation 5 "
                                         "title bold on/off"]) \
                                         .replace(" ","") \
                                         .lower()
        except:
            print("\nCheck entries for Grouping annotation 5 start, "
                  "Grouping annotation 5 title and Grouping annotation 5 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_5_title_colour = float(par_dict["Grouping "
                                                       "annotation 5 "
                                                       "title colour"])
            group_anno_5_title_font_size = float(par_dict["Grouping "
                                                          "annotation 5 "
                                                          "title font size"])    
            group_anno_5_line_colour = float(par_dict["Grouping "
                                                      "annotation 5 "
                                                      "line colour"])
            group_anno_5_line_width = float(par_dict["Grouping annotation 5 "
                                                     "line width"])    
            group_anno_5_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 5 "
                                                    "line start x"])
            group_anno_5_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 5 "
                                                              "line start y"])
            group_anno_5_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 5 line end x"])
            group_anno_5_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "5 line end y"])
            group_anno_5_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 5 "
                                                         "tag end x"])
            group_anno_5_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 5 "
                                                         "tag end y"])
            group_anno_5_corr = float(par_dict["Grouping annotation 5 tag "
                                               "correction"])
            group_anno_5_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 5 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 5 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G5")
        group_lw.append(group_anno_5_line_width)
        group_corr.append(group_anno_5_corr)
        group_corr_line.append(group_anno_5_line_y_correction)
    
        # Further grouping error checks
        if group_anno_5_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 5 title bold on/off "
                  "in Parameter file is required. Entry should be either 'on'"
                  " or 'off'.")
            sys.exit()
            
        if group_anno_5_title_colour < 0 or group_anno_5_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 5 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_5_line_colour < 0 or group_anno_5_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 5 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
                    
    ###########################################################################
    # Group 6 annotation.
    if group_anno_6 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G6_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 6" in str(k)} 
    
        # Check grouping entries exist
        for k,v in par_dict_G6_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
        # Check grouping entries
        try:
            group_anno_6_start = str(par_dict["Grouping annotation 6 start"]) \
                                    .strip()
            group_anno_6_title = str(par_dict["Grouping annotation 6 title"]) \
                                    .strip()
            group_anno_6_title_bold = str(par_dict["Grouping annotation 6 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 6 start, "
                  "Grouping annotation 6 title and Grouping annotation 6 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_6_title_colour = float(par_dict["Grouping "
                                                       "annotation 6 "
                                                       "title colour"])
            group_anno_6_title_font_size = float(par_dict["Grouping "
                                                          "annotation 6 "
                                                          "title font size"])    
            group_anno_6_line_colour = float(par_dict["Grouping annotation 6 "
                                                      "line colour"])
            group_anno_6_line_width = float(par_dict["Grouping annotation 6 "
                                                     "line width"])    
            group_anno_6_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 6 "
                                                    "line start x"])
            group_anno_6_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 6 "
                                                              "line start y"])
            group_anno_6_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 6 line end x"])
            group_anno_6_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "6 line end y"])
            group_anno_6_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 6 "
                                                   "tag end x"])
            group_anno_6_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 6 "
                                                         "tag end y"])
            group_anno_6_corr = float(par_dict["Grouping annotation 6 tag "
                                               "correction"])
            group_anno_6_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 6 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 6 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G6")
        group_lw.append(group_anno_6_line_width)
        group_corr.append(group_anno_6_corr)
        group_corr_line.append(group_anno_6_line_y_correction)
    
        # Further error checks of grouping entries
        if group_anno_6_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 6 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or "
                  "'off'.")
            sys.exit()
            
        if group_anno_6_title_colour < 0 or group_anno_6_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 6 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_6_line_colour < 0 or group_anno_6_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 6 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 7 annotation.
    if group_anno_7 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G7_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 7" in str(k)} 
    
        # Check grouping entries exist
        for k,v in par_dict_G7_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
                
        # Error check grouping entries 
        try:
            group_anno_7_start = str(par_dict["Grouping annotation 7 start"]) \
                                    .strip()
            group_anno_7_title = str(par_dict["Grouping annotation 7 title"]) \
                                    .strip()
            group_anno_7_title_bold = str(par_dict["Grouping annotation 7 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 7 start, "
                  "Grouping annotation 7 title and Grouping annotation 7 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_7_title_colour = float(par_dict["Grouping "
                                                       "annotation 7 "
                                                       "title colour"])
            group_anno_7_title_font_size = float(par_dict["Grouping "
                                                          "annotation 7 "
                                                          "title font size"])    
            group_anno_7_line_colour = float(par_dict["Grouping "
                                                      "annotation 7 "
                                                      "line colour"])
            group_anno_7_line_width = float(par_dict["Grouping annotation 7 "
                                                     "line width"])    
            group_anno_7_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 7 "
                                                    "line start x"])
            group_anno_7_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 7 "
                                                              "line start y"])
            group_anno_7_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 7 line end x"])
            group_anno_7_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "7 line end y"])
            group_anno_7_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 7 "
                                                   "tag end x"])
            group_anno_7_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 7 "
                                                         "tag end y"])
            group_anno_7_corr = float(par_dict["Grouping annotation 7 tag "
                                               "correction"])
            group_anno_7_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 7 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 7 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G7")
        group_lw.append(group_anno_7_line_width)
        group_corr.append(group_anno_7_corr)
        group_corr_line.append(group_anno_7_line_y_correction)
    
        # Further error checks of grouping entries
        if group_anno_7_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 7 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or "
                  "'off'.")
            sys.exit()
            
        if group_anno_7_title_colour < 0 or group_anno_7_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 7 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_7_line_colour < 0 or group_anno_7_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 7 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 8 annotation.
    if group_anno_8 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G8_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 8" in str(k)} 
    
        for k,v in par_dict_G8_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
        
        # Error check grouping entries
        try:
            group_anno_8_start = str(par_dict["Grouping annotation 8 start"]) \
                                    .strip()
            group_anno_8_title = str(par_dict["Grouping annotation 8 title"]) \
                                    .strip()
            group_anno_8_title_bold = str(par_dict["Grouping annotation 8 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 8 start, "
                  "Grouping annotation 8 title and Grouping annotation 8 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_8_title_colour = float(par_dict["Grouping "
                                                       "annotation 8 "
                                                       "title colour"])
            group_anno_8_title_font_size = float(par_dict["Grouping "
                                                          "annotation 8 "
                                                          "title font size"])    
            group_anno_8_line_colour = float(par_dict["Grouping annotation 8 "
                                                      "line colour"])
            group_anno_8_line_width = float(par_dict["Grouping annotation 8 "
                                                     "line width"])    
            group_anno_8_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 8 "
                                                    "line start x"])
            group_anno_8_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 8 "
                                                              "line start y"])
            group_anno_8_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 8 line end x"])
            group_anno_8_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "8 line end y"])
            group_anno_8_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 8 "
                                                   "tag end x"])
            group_anno_8_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 8 "
                                                         "tag end y"])
            group_anno_8_corr = float(par_dict["Grouping annotation 8 tag "
                                               "correction"])
            group_anno_8_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 8 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 8 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G8")
        group_lw.append(group_anno_8_line_width)
        group_corr.append(group_anno_8_corr)
        group_corr_line.append(group_anno_8_line_y_correction)
    
        # Further error checks on grouping entries
        if group_anno_8_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 8 title bold on/off "
                  "in Parameter file is required. Entry should be either 'on'"
                  " or 'off'.")
            sys.exit()
            
        if group_anno_8_title_colour < 0 or group_anno_8_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 8 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_8_line_colour < 0 or group_anno_8_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 8 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 9 annotation.
    if group_anno_9 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G9_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation 9" in str(k)} 
    
        for k,v in par_dict_G9_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
        
        # Error check grouping entries
        try:
            group_anno_9_start = str(par_dict["Grouping annotation 9 start"]) \
                                    .strip()
            group_anno_9_title = str(par_dict["Grouping annotation 9 title"]) \
                                    .strip()
            group_anno_9_title_bold = str(par_dict["Grouping annotation 9 "
                                         "title bold on/off"]) \
                                         .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 9 start, "
                  "Grouping annotation 9 title and Grouping annotation 9 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_9_title_colour = float(par_dict["Grouping "
                                                       "annotation 9 "
                                                       "title colour"])
            group_anno_9_title_font_size = float(par_dict["Grouping "
                                                          "annotation 9 "
                                                          "title font size"])    
            group_anno_9_line_colour = float(par_dict["Grouping "
                                                      "annotation 9 "
                                                      "line colour"])
            group_anno_9_line_width = float(par_dict["Grouping "
                                                     "annotation 9 "
                                                     "line width"])    
            group_anno_9_line_x_offset_start = float(par_dict["Grouping "
                                                    "annotation 9 "
                                                    "line start x"])
            group_anno_9_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation 9 "
                                                              "line start y"])
            group_anno_9_line_x_offset_end = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 9 line end x"])
            group_anno_9_line_y_offset_end = float(par_dict["Grouping "
                                                            "annotation "
                                                            "9 line end y"])
            group_anno_9_line_x_tag_end = float(par_dict["Grouping "
                                                         "annotation 9 "
                                                         "tag end x"])
            group_anno_9_line_y_tag_end = float(par_dict["Grouping "
                                                         "annotation 9 "
                                                         "tag end y"])
            group_anno_9_corr = float(par_dict["Grouping annotation 9 tag "
                                               "correction"])
            group_anno_9_line_y_correction = float(par_dict["Grouping "
                                                            "annotation"
                                                            " 9 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 9 annotation in Parameter file. "
                  "One of the numeric entries is missing or erroneous. Check "
                  "entries and formats.")
            sys.exit()
        
        group_list.append("G9")
        group_lw.append(group_anno_9_line_width)
        group_corr.append(group_anno_9_corr)
        group_corr_line.append(group_anno_9_line_y_correction)
    
        # Further grouping entry error checks
        if group_anno_9_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 9 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or"
                  " 'off'.")
            sys.exit()
            
        if group_anno_9_title_colour < 0 or group_anno_9_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 9 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_9_line_colour < 0 or group_anno_9_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 9 line colour in "
                  "Parameter file is out of bounds. Refer to manual for "
                  "colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    # Group 10 annotation.
    if group_anno_10 == "on":
        
        # Create dictionary of grouping entries
        par_dict_G10_values = {k: v for k, v in par_dict.items() \
                          if "Grouping annotation *10" in str(k)} 
        
        # Check entries exist
        for k,v in par_dict_G10_values.items():
            if pd.isnull(v) == True:
                print(f"Entry missing for {k}.")
                sys.exit() 
        
        # Error check grouping entries
        try:
            group_anno_10_start = str(par_dict["Grouping annotation *10 "
                                               "start"]).strip()
            group_anno_10_title = str(par_dict["Grouping annotation *10 "
                                               "title"]). strip()
            group_anno_10_title_bold = str(par_dict["Grouping annotation"
                                                    " *10 title bold "
                                                    "on/off"]) \
                                                    .replace(" ","").lower()
        except:
            print("\nCheck entries for Grouping annotation 10 start, "
                  "Grouping annotation 10 title and Grouping annotation 10 "
                  "title bold on/off. One of these is erroneous. Check entry "
                  "and format.")
            sys.exit()
        
        try:
            group_anno_10_title_colour = float(par_dict["Grouping "
                                                        "annotation *10 "
                                                       "title colour"])
            group_anno_10_title_font_size = float(par_dict["Grouping "
                                                           "annotation "
                                                           "*10 title "
                                                           "font size"])    
            group_anno_10_line_colour = float(par_dict["Grouping "
                                                       "annotation *10 "
                                                      "line colour"])
            group_anno_10_line_width = float(par_dict["Grouping "
                                                      "annotation *10 "
                                                      "line width"])    
            group_anno_10_line_x_offset_start = float(par_dict["Grouping "
                                                               "annotation "
                                                               "*10 "
                                                               "line start x"])
            group_anno_10_line_y_offset_start = float(par_dict["Grouping "
                                                              "annotation *10 "
                                                              "line start y"])
            group_anno_10_line_x_offset_end = float(par_dict["Grouping "
                                                             "annotation"
                                                             " *10 line "
                                                             "end x"])
            group_anno_10_line_y_offset_end = float(par_dict["Grouping "
                                                             "annotation"
                                                             " *10 line "
                                                             "end y"])
            group_anno_10_line_x_tag_end = float(par_dict["Grouping "
                                                          "annotation "
                                                          "*10 tag end x"])
            group_anno_10_line_y_tag_end = float(par_dict["Grouping "
                                                          "annotation "
                                                          "*10 tag end y"])
            group_anno_10_corr = float(par_dict["Grouping annotation *10 tag "
                                               "correction"])
            group_anno_10_line_y_correction = float(par_dict["Grouping "
                                                             "annotation"
                                                            " *10 line "
                                                            "correction"])
        except:
            print("\nCheck entries for Group 10 annotation in Parameter file."
                  " One of the numeric entries is missing or erroneous. Check"
                  " entries and formats.")
            sys.exit()
        
        group_list.append("G10")
        group_lw.append(group_anno_10_line_width)
        group_corr.append(group_anno_10_corr)
        group_corr_line.append(group_anno_10_line_y_correction)
    
        # Further grouping error checks
        if group_anno_10_title_bold not in ["on","off"]:
            print("\nEntry for Grouping annotation 10 title bold on/off in "
                  "Parameter file is required. Entry should be either 'on' or"
                  " 'off'.")
            sys.exit()
            
        if group_anno_10_title_colour < 0 or group_anno_10_title_colour > \
            col_max:
            print("\nEntry for Grouping annotation 10 title colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
        if group_anno_10_line_colour < 0 or group_anno_10_line_colour > \
            col_max:
            print("\nEntry for Grouping annotation 10 line colour in "
                  "Parameter file is out of bounds. Refer to manual for"
                  " colour codes. Colour codes presently range from 1-23.")
            sys.exit()
            
    ###########################################################################
    ###########################################################################
    # Palaeo plots often have zones drawn. Zones can be specified in the 
    # Parameter file. Obtain parameters regarding zones and check user entries
    # as much as possible.
    zones_on_off = par_dict["Zones on/off**"].replace(" ","").lower() 
    
    if zones_on_off not in ["on", "off"] or pd.isnull(zones_on_off) == True:
        print("\nEntry for Zones on/off in Parameter file must be either 'on'"
              " or 'off'.")
        sys.exit()
        
    if zones_on_off == "on":
        # Obtain depths of zones from Parameter file and check all entries
        try:
            zone_lines = par_dict["Zone depths"].replace(" ","").split(",")
            zone_lines = [float(x) for x in zone_lines]
        except:
            print("\nEntry required for Zone depths in Parameter file. Either"
                  " entry is missing or there is a formatting problem. Check "
                  "entry.")
            sys.exit()
        
        # Zone main title font and rotation.
        zone_title = par_dict["Zone title"]
        
        try:
            zone_title_font = float(par_dict["Zone title font size"] \
                                    .replace(" ",""))
        except:
            print("\nEntry required for Zone title font size in Parameter"
                  " file. Check format and that there is a numeric entry.")
            sys.exit()
            
        try:
            zone_title_rot = float(par_dict["Zone title rotation"] \
                                   .replace(" ",""))
        except:
            print("\nEntry required for Zone title font rotation in Parameter"
                  " file.Check format and that there is a numeric entry.")
            sys.exit()
            
        if zone_title_rot < 0 or zone_title_rot > 360:
            print("\nZone title rotation entry in Parameter file is out of "
                  "bounds. Requires entry between 0 and 360 degrees.")
            sys.exit()
            
        try:
            zone_title_colour = float(par_dict["Zone title colour"] \
                                     .replace(" ",""))
        except:
            print("\nEntry required for Zone title colour in Parameter file. "
                  "Check format and that there is a numeric entry.")
            sys.exit()
            
        try:
            zone_title_bold = par_dict["Zone title bold on/off"] \
                          .replace(" ","").lower()
        except:
            print("\nEntry required for Zone title bold on/off in Parameter "
                  "file. Entry should be 'on' or 'off'.")
            sys.exit()
            
        if zone_title_bold not in ["on", "off"]:
            print("\nZone title bold on/off entry in Parameter file is "
                  "incorrect. Entry should be 'on' or 'off'.")
            sys.exit()
            
        try:
            par_col_list_values_1 = par_dict["Zone line col list"].split(",")
            par_col_list_values_1 = [float(x) for x in par_col_list_values_1]
        except: 
                print("\nZone line col list entries in Parameter file are "
                      "missing or incorrect.")
                sys.exit()
        
        if any (i < 0 or i > col_max or pd.isnull(i) for i in \
                par_col_list_values_1):
            print("\nZone line col list entries in Parameter file are "
                  "out of bounds or missing.")
            sys.exit()
    
        if pd.isnull(par_dict["Zone line col list"]) == True:
            print("\n Colour entries for Zone line col list in Parameter file"
                  " are required.")
            sys.exit()
    
        # Line style width and colour for zone lines.
        # Valid entries are 1,2,3 or 4". See manual for definitions.
        try:
            zone_line_style = par_dict["Zone line style"].replace(" ","") \
                                       .split(",")
            zone_line_style  = [float(x) for x in zone_line_style]
        except:
            print("\nEntry required for Zone line style in Parameter file."
                  " Check entries.") 
            sys.exit()
    
        if any (i < 1 or i > 4 or pd.isnull(i) for i in \
                zone_line_style):
            print("\nZone line style list entries in Parameter file are"
                  " out of bounds or missing.")
            sys.exit()        
    
        try:
            zone_line_width = par_dict["Zone line width"].replace(" ","") \
                                       .split(",")
            zone_line_width = [float(x) for x in zone_line_width]
        except:
            print("\nEntries required for Zone line width in Parameter file.")
            sys.exit()
            
        try:
            zone_line_colour = par_dict["Zone line col list"]. \
                                        replace(" ","").split(",") 
            zone_line_colour  = [float(x) for x in zone_line_colour]
        except:
            print("\nEntry required for Zone line col list in Parameter file.")
            sys.exit()
            
        try:
            zone_boundary_line_top = par_dict["Zone boundary line left "
                                              "on/off"].replace(" ","").lower()
            zone_boundary_line_bottom = par_dict["Zone boundary line right "
                                                "on/off"].replace(" ",""). \
                                                 lower()
            zone_boundary_line_left = par_dict["Zone boundary line top "
                                               "on/off"].replace(" ",""). \
                                                lower()
            zone_boundary_line_right = par_dict["Zone boundary line bottom "
                                                "on/off"].replace(" ",""). \
                                                 lower()        
        except:
            print("\nCheck all four of the Zone boundary line on/off"
                  " entries in the Parameter file.")
            sys.exit()
            
        zone_boundary_line_list = [zone_boundary_line_top, \
                                   zone_boundary_line_bottom, \
                                   zone_boundary_line_left, \
                                   zone_boundary_line_right]
            
        if any(pd.isnull(i) or i not in ["on","off"] for i in \
               zone_boundary_line_list ):
            print("\nCheck all four of the Zone boundary line on/off"
                  " entries in the Parameter file. Entry should be"
                  " 'on' or 'off'.")
            sys.exit()
            
        try:
            zone_boundary_line_style = float(par_dict["Zone boundary line "
                                            "style"].replace(" ",""))
        
            zone_boundary_line_colour = float(par_dict["Zone boundary line"
                                              " colour"].replace(" ",""))
                
            zone_boundary_line_width = float(par_dict["Zone boundary line "
                                            "width"].replace(" ",""))   
        except:
            print("\nProblem with Zone boundary entry. Check all zone"
                  " boundary entries and formats.")
            sys.exit()
            
        if zone_boundary_line_style < 0 or zone_boundary_line_style > 4 \
            or pd.isnull(zone_boundary_line_style) == True:
            print("\nZone boundary line style entry in Parameter file is "
                  "incorrect, missing or out of bounds (1-4).")
            sys.exit() 
            
        if zone_boundary_line_colour <= 0 or zone_boundary_line_colour > \
            col_max or pd.isnull(zone_boundary_line_colour) == True:
            print("\nZone boundary line colour entry in Parameter file is"
                  " out of bounds or missing.")
            sys.exit()
               
        # Obtain parameters for individual zone labels from Parameter file and 
        # check.
        try:
            zone_labels_on_off = par_dict["Zone labels on/off"] \
                             .replace(" ","").lower()
        except:
            print("\nZone labels on/off entry in Parameter file is incorrect."
                  "Entry should be either 'on' or 'off.'")
            sys.exit()
            
        if zone_labels_on_off not in ["on", "off"]:
            print("\nZone labels on/off needs to be either 'on' or 'off'.")
            sys.exit()
                             
        if zone_labels_on_off == "on":
            try:
                zone_lab_font = float(par_dict["Zone label font size"]. \
                              replace(" ",""))
            except:
                print("\nEntry for zone label font size in Parameter file is "
                      "required. Check entry and format.")
                sys.exit()
                
            try:
                zone_lab_rot = float(par_dict["Zone label rotation"]\
                                     .replace(" ",""))
            except:
                print("\nEntry for zone label rotation in Parameter file "
                      "required. Check entry and format.")
                sys.exit()
                
            if zone_lab_rot < 0 or zone_lab_rot > 360:
                print("\nZone label rotation in Parameter file must be"
                      " between 0 and 360 degrees.")
                sys.exit()
                
            try:
                zone_lab_pos = float(par_dict["Zone label position"]\
                                     .replace(" ",""))
            except:
                print("\nEntry for zone label position in Parameter file "
                      "required. Check entry and format.")
                sys.exit() 
    
            try:
                zone_label_colour = float(par_dict["Zone label colour"] \
                                  .replace(" ",""))
            except:
                print("\nEntry for zone label colour in Parameter file "
                      "required. Check entry and format.")
                sys.exit() 
    
            if zone_label_colour < 0 or zone_label_colour > col_max:
                print("\nZone label colour code in Parameter file must be "
                      "between 1 - 23. See colour codes in manual.")
                sys.exit()
                
            try:
                zone_label_bold = par_dict["Zone label bold on/off"]. \
                                          replace(" ","").lower()
            except:
                print("\nEntry for zone label bold on/off in Parameter file "
                      "required.")
                sys.exit() 
    
            if zone_label_bold not in ["on", "off"]:
                print("\nZone label bold entry in Parameter file must "
                      "be 'on' or 'off'.")
                sys.exit()            
              
            try:
                zone_lab_pos_corr = float(par_dict["Zone label position "
                                                   "correction"]. \
                                                    replace(" ",""))
            except:
                print("\nEntry for zone label position in Parameter file "
                      "required. If no correction required enter a zero."
                      " Check entry and format.")
                sys.exit()
    
            # Obtain names of zones from Parameter file and check.
            zones = []
            
            try:
                zone_labels = par_dict["Zone labels"].split(",")
            except:
                print("\nZone labels entry in Parameter file is incorrect."
                      " Check entries. Is the entry blank?")
                sys.exit()
    
        # Alter here if ticks are specified for depth axis on zones too by 
        # X ticks depth axis only** being off in Parameter file. Obtain 
        # entries and check.
        if x_all_ticks == "off":
            try:
                zone_x_tick_maj_colour = float(par_dict \
                                               ["Zone X major tick colour"] \
                                               .replace(" ",""))                
            except:
                print("\nZone X major tick colour entry in Parameter file is"
                      " incorrect.")
                sys.exit()
                
            if zone_x_tick_maj_colour < 0 or zone_x_tick_maj_colour > \
                col_max or pd.isnull(zone_x_tick_maj_colour) == True:
                print("\nZone X major tick colour entry in Parameter file"
                      " is out of bounds or missing.")
                sys.exit()  
                    
            if x_minor_ticks_on_off == "on":
                try:
                    zone_x_tick_min_colour = \
                        float(par_dict["Zone X minor tick colour"] \
                                       .replace(" ",""))
                except:
                    print("\nZone X minor tick colour entry in Parameter"
                          " file is incorrect.")
                    sys.exit() 
                
                if zone_x_tick_min_colour <= 0 or zone_x_tick_min_colour \
                    > col_max or pd.isnull(zone_x_tick_min_colour) == True:
                    print("\nZone X minor tick colour entry in Parameter"
                          " file is out of bounds or missing.")
                    sys.exit()
    
        # Further error checking user input for zones.
        for zlc in zone_line_colour:
            if zlc > col_max or zlc < 1:
                print("")
                print(f"\nZone line colour in Parameter file is out of "
                      f"range (1 - {col_max}).")
                sys.exit()
                
        for zls in zone_line_style:
            if zls > 4 or zls < 1:
                print("")
                print("\nZone line style in Parameter file is out of range. "
                      "(1 - 4)")
                sys.exit()
    
    ###########################################################################
    # Obtain zone depths and upmost and deepest depths from Parameter file and 
    # Input file.
    if zones_on_off == "on":
        zones = zone_lines
        zones.insert(0,0)
        zones.insert(len(zones) + 1, np.max(data["Depth"] [2::]))
        zones = zones[::-1]
        
        # Create a central location for the zone labels in the zone column
        # of the plot.
        zone_place = []
        
        a = 0
        
        for Z in range(len(zones) - 1):
            zone_place.append(((zones[a]-zones[a + 1]) / 2 + zones[a + 1]))
            a+=1
            
        zone_place = zone_place[::-1]
        
        # Check if zones are to be used there are the correct number of data 
        # points. Should be one more label than there are lines. Check right
        # number of data points for style, width etc.
        if zones_on_off == "on":
            if len(zone_lines[1:-1]) - len(zone_labels) != -1:
                print("")
                print("\nError in zonation, too many or too few zone names / "
                      "lines in Parameter file.")
                sys.exit()
                
            if len(zone_line_style) != len(zone_line_width) or \
                len(zone_line_style) != len(zone_lines[1:-1]):
                print("")
                print("\nError in zonation, too many or too few zone styles"
                      " or line widths in Parameter file.")
                sys.exit()
                
            if len(zone_line_width) != len(zone_line_colour) or \
                len(zone_line_width) != len(zone_lines[1:-1]):
                print("")
                print("\nError in zonation, too many or too few line colours"
                      " or line widths in Parameter file.")
                sys.exit()
                
            if len(zone_line_style) != len(zone_line_colour) or \
                len(zone_line_style) != len(zone_lines[1:-1]):
                print("")
                print("\nError in zonation, too many or too few zone styles"
                      " or colours in Parameter file.")
                sys.exit()
    
    # Alter diff ratios if stack plots are specified as well as zones and if 
    # without zones. Give default value of 1 for now. This is used to give
    # plots their scaled widths.
    if zones_on_off == "on":
        if num_stack_plots == 1:
            diff_list_ratios [1] = 1
            
        if num_stack_plots == 2:
            diff_list_ratios [1] = 1
            diff_list_ratios [2] = 1
            
    if zones_on_off == "off":
        if num_stack_plots == 1:
            diff_list_ratios [0] = 1
            
        if num_stack_plots == 2:
            diff_list_ratios [0] = 1
            diff_list_ratios [1] = 1
    
    ###########################################################################
    ###########################################################################
    # Create the individual plots. Below is repeated code depending on how 
    # many taxa there are. The program is limited to 60 taxa. Beyond 60 it is 
    # not really legible on an A4 piece of paper. 
    
    # Obtain information re the overall size of figure required and font to be
    # used throughout changed here from cm to inches.
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = overall_x / 2.54
    fig_size[1] = overall_y / 2.54
    
    plt.rcParams["figure.figsize"] = fig_size
    plt.rcParams.update({'font.family': font_style})
    
    # Set up each basic plot based on number of taxa to be plotted.
    if zones_on_off == "off":
        diff_list_ratios_dict.pop("Zones")
                                  
    diff_list_ratios = list(diff_list_ratios_dict.values())
    diff_list_ratios = diff_list_ratios [::-1]
    
    fig = plt.figure(facecolor = "white", edgecolor = "none")
    
    gs = GridSpec(len(data_list), 1, width_ratios = [1], \
                  height_ratios = (diff_list_ratios), \
                  hspace = h_space, \
                  left = float(par_dict["Overall title gap"]))
    
    if len(data_list) == 1:
        ax1 = fig.add_subplot(gs[0])
        
        ax_list = [ax1]
        
    elif len(data_list) == 2:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        
        ax_list = [ax1, ax2]
        
    elif len(data_list) == 3:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        
        ax_list = [ax1, ax2, ax3]
        
    elif len(data_list) == 4:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        
        ax_list = [ax1, ax2, ax3, ax4]
        
    elif len(data_list) == 5:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5]
        
    elif len(data_list) == 6:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6]
        
    elif len(data_list) == 7:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7]
        
    elif len(data_list) == 8:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
        
    elif len(data_list) == 9:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
        
    elif len(data_list) == 10:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]
        
    elif len(data_list) == 11:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]
        
    elif len(data_list) == 12:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12]
        
    elif len(data_list) == 13:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13]
        
    elif len(data_list) == 14:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14]
        
    elif len(data_list) == 15:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15]
        
    elif len(data_list) == 16:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16]
        
    elif len(data_list) == 17:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17]
        
    elif len(data_list) == 18:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18]
        
    elif len(data_list) == 19:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7,ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19]
        
    elif len(data_list) == 20:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20]
        
    elif len(data_list) == 21:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21]
        
    elif len(data_list) == 22:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22]
        
    elif len(data_list) == 23:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23]
        
    elif len(data_list) == 24:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24]
        
    elif len(data_list) == 25:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25]
            
    elif len(data_list) == 26:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26]
            
    elif len(data_list) == 27:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27]
            
    elif len(data_list) == 28:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28]
            
    elif len(data_list) == 29:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26,  ax27, ax28, ax29]
            
    elif len(data_list) == 30:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, ax30]
            
    elif len(data_list) == 31:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31]
            
    elif len(data_list) == 32:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32]
            
    elif len(data_list) == 33:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33] 
            
    elif len(data_list) == 34:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34] 
            
    elif len(data_list) == 35:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35] 
            
    elif len(data_list) == 36:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36]  
            
    elif len(data_list) == 37: 
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37]  
            
    elif len(data_list) == 38:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38]  
            
    elif len(data_list) == 39:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39]     
            
    elif len(data_list) == 40:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40]          
            
    elif len(data_list) == 41:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41]   
            
    elif len(data_list) == 42:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42]   
            
    elif len(data_list) == 43:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43]
             
    elif len(data_list) == 44:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44] 
            
    elif len(data_list) == 45:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45]    
            
    elif len(data_list) == 46:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46]   
            
    elif len(data_list) == 47:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47]   
            
    elif len(data_list) == 48:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48] 
            
    elif len(data_list) == 49:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49]   
            
    elif len(data_list) == 50:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49]) 
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50] 
            
    elif len(data_list) == 51:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51]    
            
    elif len(data_list) == 52:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52]   
    
    elif len(data_list) == 53:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])   
        ax25 = fig.add_subplot(gs[24]) 
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26]) 
        ax28 = fig.add_subplot(gs[27]) 
        ax29 = fig.add_subplot(gs[28]) 
        ax30 = fig.add_subplot(gs[29]) 
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32]) 
        ax34 = fig.add_subplot(gs[33]) 
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36]) 
        ax38 = fig.add_subplot(gs[37]) 
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39]) 
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41]) 
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44]) 
        ax46 = fig.add_subplot(gs[45]) 
        ax47 = fig.add_subplot(gs[46]) 
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53]  
        
    elif len(data_list) == 54:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
    
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54]
        
    elif len(data_list) == 55:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
    
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55]
    
    elif len(data_list) == 56:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
        ax56 = fig.add_subplot(gs[55])
    
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55, ax56]   
    
    elif len(data_list) == 57:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36= fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
        ax56 = fig.add_subplot(gs[55])
        ax57 = fig.add_subplot(gs[56])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55, ax56, \
                   ax57]
    
    elif len(data_list) == 58:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
        ax56 = fig.add_subplot(gs[55])
        ax57 = fig.add_subplot(gs[56])
        ax58 = fig.add_subplot(gs[57])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55, ax56, \
                   ax57, ax58]  
            
    elif len(data_list) == 59:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
        ax56 = fig.add_subplot(gs[55])
        ax57 = fig.add_subplot(gs[56])
        ax58 = fig.add_subplot(gs[57])
        ax59 = fig.add_subplot(gs[58])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55, ax56, \
                   ax57, ax58, ax59]
    
    elif len(data_list) == 60:
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
        ax4 = fig.add_subplot(gs[3])
        ax5 = fig.add_subplot(gs[4])
        ax6 = fig.add_subplot(gs[5])
        ax7 = fig.add_subplot(gs[6])
        ax8 = fig.add_subplot(gs[7])
        ax9 = fig.add_subplot(gs[8])
        ax10 = fig.add_subplot(gs[9])
        ax11 = fig.add_subplot(gs[10])
        ax12 = fig.add_subplot(gs[11])
        ax13 = fig.add_subplot(gs[12])
        ax14 = fig.add_subplot(gs[13])
        ax15 = fig.add_subplot(gs[14])
        ax16 = fig.add_subplot(gs[15])
        ax17 = fig.add_subplot(gs[16])
        ax18 = fig.add_subplot(gs[17])
        ax19 = fig.add_subplot(gs[18])
        ax20 = fig.add_subplot(gs[19])
        ax21 = fig.add_subplot(gs[20])
        ax22 = fig.add_subplot(gs[21])
        ax23 = fig.add_subplot(gs[22])
        ax24 = fig.add_subplot(gs[23])
        ax25 = fig.add_subplot(gs[24])
        ax26 = fig.add_subplot(gs[25])
        ax27 = fig.add_subplot(gs[26])
        ax28 = fig.add_subplot(gs[27])
        ax29 = fig.add_subplot(gs[28])
        ax30 = fig.add_subplot(gs[29])
        ax31 = fig.add_subplot(gs[30])
        ax32 = fig.add_subplot(gs[31])
        ax33 = fig.add_subplot(gs[32])
        ax34 = fig.add_subplot(gs[33])
        ax35 = fig.add_subplot(gs[34])
        ax36 = fig.add_subplot(gs[35])
        ax37 = fig.add_subplot(gs[36])
        ax38 = fig.add_subplot(gs[37])
        ax39 = fig.add_subplot(gs[38])
        ax40 = fig.add_subplot(gs[39])
        ax41 = fig.add_subplot(gs[40])
        ax42 = fig.add_subplot(gs[41])
        ax43 = fig.add_subplot(gs[42])
        ax44 = fig.add_subplot(gs[43])
        ax45 = fig.add_subplot(gs[44])
        ax46 = fig.add_subplot(gs[45])
        ax47 = fig.add_subplot(gs[46])
        ax48 = fig.add_subplot(gs[47])
        ax49 = fig.add_subplot(gs[48])
        ax50 = fig.add_subplot(gs[49])
        ax51 = fig.add_subplot(gs[50])
        ax52 = fig.add_subplot(gs[51])
        ax53 = fig.add_subplot(gs[52])
        ax54 = fig.add_subplot(gs[53])
        ax55 = fig.add_subplot(gs[54])
        ax56 = fig.add_subplot(gs[55])
        ax57 = fig.add_subplot(gs[56])
        ax58 = fig.add_subplot(gs[57])
        ax59 = fig.add_subplot(gs[58])
        ax60 = fig.add_subplot(gs[59])
        
        ax_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, \
                   ax12, ax13, ax14, ax15, ax16, ax17, ax18, ax19, ax20, \
                   ax21, ax22, ax23, ax24, ax25, ax26, ax27, ax28, ax29, \
                   ax30, ax31, ax32, ax33, ax34, ax35, ax36, ax37, ax38, \
                   ax39, ax40, ax41, ax42, ax43, ax44, ax45, ax46, ax47, \
                   ax48, ax49, ax50, ax51, ax52, ax53, ax54, ax55, ax56, \
                   ax57, ax58, ax59, ax60]             
    
    ###########################################################################
    ###########################################################################
    # Functions for aesthetics.
    
    # Function to turn colour number to colour text this can be added to if 
    # required. See matplotlib available colours. If add extra colours increase
    # number for col_max variable.
    def colour (col):
        if col == 1:
            return "black"
        elif col == 2:
            return "gray"
        elif col == 3:
            return "dimgray"
        elif col == 4:
            return "darkgray" 
        elif col == 5:
            return "slategray"
        elif col == 6:
            return "lightgray"
        elif col == 7:
            return "red"
        elif col == 8:
            return "darkred"
        elif col == 9:
            return "orangered" 
        elif col == 10:
            return "coral"
        elif col == 11:
            return "green"
        elif col == 12:
            return "darkgreen"
        elif col == 13:
            return "olive"
        elif col == 14:
            return "lightgreen"
        elif col == 15:
            return "blue"
        elif col == 16:
            return "darkblue"
        elif col == 17:
            return "lightblue"
        elif col == 18:
            return "cyan"
        elif col == 19:
            return "yellow"
        elif col == 20:
            return "brown"
        elif col == 21: 
            return "magenta"
        elif col == 22:
            return "orange"
        elif col == 23:
            return "white"
    
    # Function to turn line_style number to line_style text. Can be added to 
    # if required.
    def line_styles (style):
        if style == 1:
            return "solid"
        elif style == 2:
            return "dotted"
        elif style == 3:
            return "dashed"
        elif style == 4:
            return "dashdot"
    
    # Function to convert marker number to marker type. Can be added to if 
    # required.
    def marker_type (mark):
        if mark == 1:
            return "o"
        elif mark == 2:
            return "x"
        elif mark == 3:
            return "^"
        elif mark == 4:
            return "v"
        elif mark == 5:
            return "D"
        elif mark == 6:
            return "*"
    
    # Bold function.
    def bold_on_off (bold):
        if bold == "ON" or bold == "on" or bold == 1:
            return "bold"
        else:
            return "normal"
    
    ###########################################################################
    ###########################################################################
    # Create individual plots for zone column if required and then each taxon
    # in turn. Order is dictated by order in the input csv file. Stack plots
    # (only 2  available at present) need to be listed as the last columns
    # of data before the zone column if zones are used.
    for taxon, graph, min_0, min_1 in zip(data_list, ax_list, \
                                          min_list_round, min_list): 
        # Y major and minor intervals.
        y_major_int = y_major_int_0
        
        if y_minor_ticks_on_off == "on":
            y_minor_int = y_minor_int_0
        
        plot_type_1 = plot_type[taxon]
                    
        # Bar colour and width for graph types 1 and 2.
        bar_col_type_1 = bar_col_type[taxon] 
        bar_col_type_2 = colour(bar_col_type_1) 
        bar_wid_1 = bar_wid[taxon] 
        bar_wid_g1_1 = bar_wid_g1[taxon]
        
        # Obtain Y title text colour.
        if title_text_on_off == "on":
            title_text_col = colour(title_text_colour) 
    
        # Obtain line style for use if graph types 2,3,4,5.
        line_type_1 = line_type[taxon] 
        line_type_2 = line_styles(line_type_1) 
    
        # Obtain line colour required for taxon if graph types 2,3,4,5.
        line_colour_type_1 = line_colour_type[taxon] 
        line_colour_type_2 = colour(line_colour_type_1) 
    
        # Obtain fill colour required for graph types 2,4.
        fill_colour_type_1 = fill_colour_type[taxon]
        fill_colour_type_2 = colour(fill_colour_type_1)
    
        # Obtain fill colour transparency required for graph types 2,4.
        fill_trans_type_1 = fill_trans_type[taxon]
        
        # Obtain marker type for graph types 5,6.
        marker_typ_type_1 = marker_typ_type[taxon]
        marker_typ_type_2 = marker_type(marker_typ_type_1)
    
        # Obtain marker face colour for graph types 5,6. 
        marker_f_col_1 =  marker_f_col[taxon]
        marker_f_col_2 = colour(marker_f_col_1)
    
        # Obtain marker edge colour for graph types 5,6.
        marker_e_col_1 = marker_e_col[taxon]
        marker_e_col_2 = colour(marker_e_col_1)
    
        # Obtain line widths marker sizes and marker edge widths.
        line_width_1 = line_width_type[taxon]
        marker_s_size_1 = marker_s_size[taxon]
        marker_e_w_wid_1 = marker_e_w_wid[taxon]
        
        # Reset the paremeters if the measure is nominated as NON_STD_SCALING.
        if taxon == non_std_scaling_1:
            yl_lim = non_std_scaling_y_min_1
            yu_lim = non_std_scaling_y_max_1
            graph.set_ylim(yl_lim, yu_lim)
            y_major_int = non_std_scaling_y_maj_int_1
            y_minor_int = non_std_scaling_y_min_int_1
       
        elif taxon == non_std_scaling_2:
            yl_lim = non_std_scaling_y_min_2
            yu_lim = non_std_scaling_y_max_2
            graph.set_ylim(yl_lim, yu_lim)
            y_major_int = non_std_scaling_y_maj_int_2
            y_minor_int = non_std_scaling_y_min_int_2
                
        elif taxon == non_std_scaling_3:
            yl_lim = non_std_scaling_y_min_3
            yu_lim = non_std_scaling_y_max_3
            graph.set_ylim(yl_lim, yu_lim)
            y_major_int = non_std_scaling_y_maj_int_3
            y_minor_int = non_std_scaling_y_min_int_3
            
        elif taxon == non_std_scaling_4:
            yl_lim = non_std_scaling_y_min_4
            yu_lim = non_std_scaling_y_max_4
            graph.set_ylim(yl_lim, yu_lim)
            y_major_int = non_std_scaling_y_maj_int_4
            y_minor_int = non_std_scaling_y_min_int_4
            
        elif taxon == non_std_scaling_5:
            yl_lim = non_std_scaling_y_min_5
            yu_lim = non_std_scaling_y_max_5
            graph.set_ylim(yl_lim, yu_lim)
            y_major_int = non_std_scaling_y_maj_int_5
            y_minor_int = non_std_scaling_y_min_int_5
        else:
            yl_lim = np.round(data_2[taxon].min(), decimals =-1)
            yu_lim = np.round(data_2[taxon].max(), decimals =-1)
            y_major_int = y_major_int 
    
            if yu_lim < data_2[taxon].max():
                yu_lim = yu_lim + 5 
                graph.set_ylim(yl_lim, yu_lim)
    
    ###########################################################################
    ###########################################################################
        # Create column area for zones if required.
        if plot_type_1 == 0:
            yl_lim = 0
    
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
            
            if y_ticks_l_r == "on" or y_ticks_l_r == "off" :
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = False, width = y_major_tick_wid, \
                                  length = y_major_tick_len) 
                
                if y_minor_ticks_on_off == "on" or \
                    y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True)
                                      
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(zone_x_tick_maj_colour))
                
                if  x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(zone_x_tick_min_colour))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if  x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', \
                              labelbottom = False, rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', \
                              labelright = False, labelleft = False, \
                              rotation = y_lab_rot) 
            
            for axis in ['top','bottom','left','right']:
                graph.spines[axis].set_linewidth(zone_boundary_line_width)
                graph.spines[axis].set_linestyle(line_styles \
                                                 (zone_boundary_line_style))
                graph.spines[axis].set_color(colour \
                                             (zone_boundary_line_colour))
                       
            if zone_boundary_line_top == "on":
                graph.spines['top'].set_visible(True)
            else:
                graph.spines['top'].set_visible(False)
    
            if zone_boundary_line_bottom == "on":
                graph.spines['bottom'].set_visible(True)
            else:
                graph.spines['bottom'].set_visible(False)
                
            if zone_boundary_line_left == "on":
                graph.spines['left'].set_visible(True)
            else:
                graph.spines['left'].set_visible(False)
                
            if zone_boundary_line_right == "on":
                graph.spines['right'].set_visible(True)
            else:
                graph.spines['right'].set_visible(False)
                
            graph.tick_params(left = False)
            graph.tick_params(top = False)
            graph.tick_params(labelleft = False)
            graph.tick_params(labelright = False)
            
            if x_all_ticks == "on":
                graph.tick_params(bottom = False)
                
            if x_all_ticks == "off":
                graph.tick_params(bottom = True)
                
            if pd.isnull(zone_title) == False:
                graph.set_ylabel(zone_title, fontsize = zone_title_font, \
                                 rotation = zone_title_rot, \
                                 weight = bold_on_off(zone_title_bold), \
                                 color = colour(zone_title_colour))
       
                graph.yaxis.labelpad = y_lab_gap + 5
            else:
                graph.set_ylabel(" ", fontsize = zone_title_font, \
                                 rotation = zone_title_rot, \
                                 color = colour(zone_title_colour))
    
            if zones_on_off == "on":
                x_limit_diff_adj = x_limit_diff / 100
                    
                if zone_labels_on_off == "on":
                    for zop, zo in zip(zone_place, zone_labels):
                        
                        if x_limit_diff_adj < 0:
                            graph.text(zop + x_limit_diff_adj - \
                                       zone_lab_pos_corr, \
                                       zone_lab_pos / 100, \
                                       zo, fontsize = zone_lab_font, \
                                       rotation = zone_lab_rot, color = \
                                       colour(zone_label_colour), \
                                       weight = bold_on_off(zone_label_bold))
                            
                        if x_limit_diff_adj > 0:
                            graph.text(zop - x_limit_diff_adj + \
                                       zone_lab_pos_corr, \
                                       zone_lab_pos / 100, \
                                       zo, fontsize = zone_lab_font, \
                                       rotation = zone_lab_rot, color = \
                                       colour(zone_label_colour), \
                                       weight = bold_on_off(zone_label_bold))
                               
    ###########################################################################
        # Error checking user inputs for taxon aethetics.
        if plot_type[taxon] > 7 or plot_type[taxon] < 1  and taxon != "Zones":
            print("")  
            print(f"\nError in plot type number designation for {taxon} in "
                  "Input file.")
            sys.exit()
            
        if taxa_taxon_c_col[taxon] > col_max or \
            taxa_taxon_c_col[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot title colour number designation for"
                  f" {taxon} in Input file.")
            sys.exit()
            
        if taxa_taxon_b_bold[taxon] > 1 or \
            taxa_taxon_b_bold[taxon] < 0 and taxon != "Zones":
            print("")
            print(f"\nError in plot title taxon bold designation for {taxon}"
                  " in Input file.")
            sys.exit()         
            
        if taxa_plot_vs_colour[taxon] > col_max or \
            taxa_plot_vs_colour[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon vertical spine colour number "
                  f"designation for {taxon} in Input file.")
            sys.exit()      
            
        if taxa_plot_vstyle[taxon] > 4 or \
            taxa_plot_vstyle[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon vertical spine style number "
                  f"designation for {taxon} in Input file.")
            sys.exit()
            
        if taxa_plot_lstyle[taxon] > 4 or \
            taxa_plot_lstyle[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon left spine style number designation"
                  f" for {taxon} in Input file.")
            sys.exit()
            
        if taxa_plot_rstyle[taxon] > 4 or \
           taxa_plot_rstyle[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon right spine style number"
                  f" designation for {taxon} in Input file.")
            sys.exit()
            
        if taxa_plot_ls_colour[taxon] > col_max or \
            taxa_plot_ls_colour[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon left spine colour number"
                  f" designation for {taxon}.")
            sys.exit()       
            
        if taxa_plot_rs_colour[taxon] > col_max or \
            taxa_plot_rs_colour[taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot taxon right spine colour number"
                  f" designation for {taxon} in Input file.")
            sys.exit()
            
        if taxa_x_tick_maj_colour [taxon] > col_max or \
            taxa_x_tick_maj_colour [taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot x major tick colour number designation"
                  f" for {taxon} in Input file.")
            sys.exit()            
            
        if taxa_x_tick_min_colour [taxon] > col_max or \
            taxa_x_tick_min_colour [taxon] < 1 and taxon != "Zones":
            print("")
            print(f"\nError in plot x minor tick colour number designation"
                  f" for {taxon} in Input file.")
            sys.exit() 
    
    ###########################################################################
    ###########################################################################
        # Create plot for first taxon to be plotted based on parameter
        # choices if  graph type is a barplot. Graph type 1.
        elif taxon == data_list_1 and plot_type_1 == 1:
    
    ###########################################################################
            # Change the Y lim if exaggeration is being used on any plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
                    
    ###########################################################################
            markerline, stemlines, baseline = graph.stem(data_2["Depth"], \
                                            data_2[taxon], \
                                            linefmt = bar_col_type_2, \
                                            markerfmt = "",  \
                                            basefmt ="black", \
                                            use_line_collection = True, \
                                            bottom = min_0)
                        
            if y_ticks_l_r == "on": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = True, \
                                      color = colour(x_lab_colour))
                        
                    graph.tick_params(axis = "x", which ='major', \
                                      direction ='out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = True)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off  == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                        
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))     
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
            
            if y_ticks_l_r == "off":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', \
                                      labelbottom =True, \
                                      color = colour(x_lab_colour))
                        
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', \
                                      labelbottom = True, \
                                      color = colour(x_lab_colour))
                        
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which ='minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which ='minor', \
                                      direction = 'out', bottom = False)
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))   
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
            
            graph.set_xlim(x_limit_top,x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot)
            
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth \
                (taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color \
                (colour(taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle \
                (line_styles(taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
            
            graph.spines['top'].set_visible(False)
                
            plt.setp(stemlines, color = bar_col_type_2, \
                     linewidth = bar_wid_g1_1)
            plt.setp(markerline, linewidth = 0, color = "black")
            plt.setp(baseline, linewidth = 0, color = "black")
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
            
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            
            graph.spines['bottom'].set_position(("data", min_0))  
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
    ###########################################################################
            # Add annotations for rc dates
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom.
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
            # Error checking for bar graph type 1.
            if bar_col_type[taxon] > col_max or \
                bar_col_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\n Bar colour number designation for {taxon} in"
                      f" Input file is out of range (1 - {col_max}).")
                sys.exit()
            
    ###########################################################################
    ###########################################################################
        # Create plot for first taxon to be plotted based on parameter
        # choices if graph type is lineplot with depth bars. Graph type 2. 
            
        elif taxon == data_list_1 and plot_type_1 == 2:
    
    ###########################################################################
            # Adjustments rerquired if exaggeration has been specified.
            if taxa_exag_type[taxon] == 3:
                if taxa_exag_line_col[taxon] not in range (1,col_max) \
                    or taxa_exag_ls[taxon] not in range (1,4):
                        
                    print("  ")
                    print (f"\n exaggeration aesthetics out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit()
                    
                graph.plot(data_2["Depth"], data_2[taxon] * taxa_exag[taxon], \
                                color = colour(taxa_exag_line_col[taxon]), \
                                linewidth = taxa_exag_lw[taxon], \
                                linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
        
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))           
                
            if taxa_exag_type[taxon] == 4:
                if taxa_exag_col[taxon] not in range (1, col_max) \
                    or taxa_exag_line_col[taxon] \
                    not in range (1, col_max) or taxa_exag_ls[taxon] \
                    not in range (1, 4) or taxa_exag_trans[taxon] * 100 \
                    not in range (0, 100):
                    
                    print("  ")    
                    print (f"\n Exaggeration aethetics are out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit()
                    
                graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                   taxa_exag[taxon], \
                                   color = colour(taxa_exag_col[taxon]), \
                                   linewidth = taxa_exag_lw[taxon], \
                                   alpha = taxa_exag_trans[taxon])
                    
                graph.plot(data_2["Depth"],data_2[taxon] * taxa_exag[taxon], \
                                color = colour(taxa_exag_line_col[taxon]), \
                                linewidth = taxa_exag_lw[taxon], \
                                linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))
    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = fill_colour_type_2, \
                               linewidth = line_width_1, \
                               alpha = fill_trans_type_1)
                
            markerline, stemlines, baseline = \
                graph.stem(data_2["Depth"], data_2[taxon], \
                          linefmt = bar_col_type_2, markerfmt = "", \
                          basefmt = "black", use_line_collection = True, \
                          bottom = min_0)
                
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color =  line_colour_type_2, \
                       linewidth = line_width_1, linestyle = line_type_2)
           
            graph.set_xlim(x_limit_top,x_limit_base)
            
            if y_ticks_l_r == "on":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out' , \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks== "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))  
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False) 
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))   
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
            
            if y_ticks_l_r =="off": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
    
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))      
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
    
            graph.set_xlim(x_limit_top,x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction= 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
            
            graph.spines['bottom'].set_linestyle \
                (line_styles(taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color \
                (colour(taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle \
                (line_styles(taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles\
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth \
                (taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)          
                            
            plt.setp(stemlines, color = bar_col_type_2, linewidth = bar_wid_1)
            plt.setp(markerline, linewidth = 0, color = "black")
            plt.setp(baseline, linewidth = 0, color = "black")    
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment ='bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
            graph.yaxis.labelpad = y_lab_gap
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            
            graph.spines['bottom'].set_position(("data", min_0))
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction ='out', \
                              labelbottom = True, \
                              rotation = x_lab_rot)
    
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
    
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom.
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
            # Error checking.
            if bar_col_type[taxon] > col_max or \
                bar_col_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nBar colour number designation for {taxon} is out"
                      f" of range (1 - {col_max}) in Input file.")
                sys.exit()
                
            if line_type[taxon] > 4 or \
                line_type[taxon] < 0  and taxon != "Zones":
                print("  ")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
        
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1  and taxon != "Zones":
                print("  ")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if fill_colour_type[taxon] > col_max or \
                fill_colour_type[taxon] < 1  and taxon != "Zones":
                print("  ")
                print(f"\nError in fill colour number for {taxon} in Input "
                      "file.")
                sys.exit() 
                
            if fill_trans_type[taxon] > 1 or \
                fill_trans_type[taxon] < 0  and taxon != "Zones":
                print("  ")
                print(f"\nError in fill colour transparency for {taxon} in "
                      "Input file.")
                sys.exit()
    
    ###########################################################################
    ###########################################################################
        # Create plot for first taxon to be plotted based on parameter choices
        # if graph type is a line plot Graph type 3.
        
        elif taxon == data_list_1 and plot_type_1 == 3:
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified.
            if taxa_exag_type[taxon] == 3:
                if taxa_exag_line_col[taxon] not in range (1, col_max) or \
                    taxa_exag_ls[taxon] not in range (1, 4):
                    print("  ")                    
                    print (f"\nExaggeration aesthetics are out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit()
                    
                graph.plot(data_2["Depth"], data_2[taxon] * \
                           taxa_exag[taxon], \
                           color = colour(taxa_exag_line_col[taxon]), \
                           linewidth = taxa_exag_lw[taxon], \
                           linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))   
            
            if taxa_exag_type[taxon] == 4:
                if taxa_exag_col[taxon] not in range (1, col_max) \
                    or taxa_exag_line_col[taxon] not in range (1, col_max) \
                    or taxa_exag_ls[taxon] not in range (1, 4) or \
                    taxa_exag_trans[taxon] * 100 not in range (0, 100):
                    print("  ")                    
                    print (f"\nExaggeration aesthetics out of bounds for"
                           f" {taxon} in Input file.")
                    sys.exit() 
                        
                graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                   taxa_exag[taxon], \
                                   color = colour(taxa_exag_col[taxon]), \
                                   linewidth = taxa_exag_lw[taxon], \
                                   alpha = taxa_exag_trans[taxon])
                    
                graph.plot(data_2["Depth"], data_2[taxon] * \
                           taxa_exag[taxon], \
                           color = colour(taxa_exag_line_col[taxon]), \
                           linewidth = taxa_exag_lw[taxon], \
                           linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1)) 
                    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = "white", linewidth = 0, alpha = 1)
            
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color =  line_colour_type_2, \
                       linewidth = line_width_1, \
                       linestyle = line_type_2)
                
            graph.set_xlim(x_limit_top, x_limit_base)
            
            if y_ticks_l_r == "on":  
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction= 'out', labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon])) 
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which ='minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))   
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
    
            if y_ticks_l_r == "off": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))   
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                        
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False) 
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))        
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
            
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
                
            graph.spines['bottom'].set_linestyle \
                (line_styles(taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth \
                (taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color\
                (colour(taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle \
                (line_styles(taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth \
                (taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle \
                (line_styles(taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)          
                
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", 0))
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom.
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
                
    ###########################################################################
            # Error checking for graph type 3.
            if line_type[taxon] > 4 or \
                line_type[taxon] < 1 and taxon != "Zones":
                print("")
                print(f"\nError in line type number {taxon} in Input file.")
                sys.exit()
                
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1  and taxon != "Zones":
                print("")
                print(f"\nError in line colour number for {taxon} in "
                      "Input file.")
                sys.exit()
    
    ###########################################################################
        # Create plot for first taxon to be plotted based on parameter 
        # choices if graph type is a line plot with solid shading below 
        # line. Graph type 4.    
        
        elif taxon == data_list_1 and plot_type_1 == 4:
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified.
            if taxa_exag_type[taxon] == 3:
                
                if taxa_exag_line_col[taxon] not in range (1, col_max) or \
                    taxa_exag_ls[taxon] not in range (1, 4):
                    print("  ")                    
                    print (f"\nExaggeration aesthetics are out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit()
                
                graph.plot(data_2["Depth"], data_2[taxon] * \
                           taxa_exag[taxon], \
                           color = colour(taxa_exag_line_col[taxon]), \
                           linewidth = taxa_exag_lw[taxon], \
                           linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))   
    
            if taxa_exag_type[taxon] == 4:
                if taxa_exag_col[taxon] not in range (1, col_max) \
                    or taxa_exag_line_col[taxon] not in range (1, col_max) \
                    or taxa_exag_ls[taxon] not in range (1, 4) or \
                    taxa_exag_trans[taxon] * 100 not in range (0, 100):
                    print("  ")                    
                    print (f"\nExaggeration aesthetics are out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit() 
                        
                graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                   taxa_exag[taxon], \
                                   color = colour(taxa_exag_col[taxon]), \
                                   linewidth = taxa_exag_lw[taxon], \
                                   alpha = taxa_exag_trans[taxon])
                    
                graph.plot(data_2["Depth"], data_2[taxon] * \
                           taxa_exag[taxon], \
                           color = colour(taxa_exag_line_col[taxon]), \
                           linewidth = taxa_exag_lw[taxon], \
                           linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))
                    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = fill_colour_type_2, \
                               linewidth = line_width_1, \
                               alpha = fill_trans_type_1)
                
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color = line_colour_type_2, \
                       linewidth = line_width_1, linestyle = line_type_2)
            
            graph.set_xlim(x_limit_top, x_limit_base)
    
            if y_ticks_l_r == "on": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which ='major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
                        
            if y_ticks_l_r == "off":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', labelbottom = False)
                    
                    graph.tick_params(axis = "x",which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon])) 
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False,\
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction ='out', bottom = False)
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                                 [taxon]))
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
            
            graph.set_xlim(x_limit_top,x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)          
                
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", 0))
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
            # Error checking for graph type 4.
            if line_type[taxon] > 4 or \
                line_type[taxon] < 0 and taxon != "Zones":
                print("  ")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if fill_colour_type[taxon] > col_max or \
                fill_colour_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in fill colour number for {taxon} in Input "
                      "file.")
                sys.exit()
    
            if fill_trans_type[taxon] > 1 or \
                fill_trans_type[taxon] < 0 and taxon != "Zones":
                print("  ")
                print(f"\nError in fill colour transparency for {taxon} in"
                      " Input file.")
                sys.exit()
    
    ###########################################################################
    ###########################################################################
        # Create plot for taxon to be plotted based on parameter chouces if
        # graph type is a line and marker plot. Graph type 5.
        
        elif taxon == data_list_1 and plot_type_1 == 5:
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified to any
            # plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
    
    ###########################################################################
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color = line_colour_type_2, \
                       linewidth = line_width_1, \
                       linestyle = line_type_2, \
                       marker = marker_typ_type_2, \
                       ms = marker_s_size_1, \
                       markeredgecolor = marker_e_col_2, \
                       markerfacecolor = marker_f_col_2, \
                       markeredgewidth = marker_e_w_wid_1)
           
            graph.set_xlim(x_limit_top, x_limit_base)
            
            if y_ticks_l_r == "on":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom =False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction ='out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))  
    
                if y_minor_ticks_on_off == "on":
                    
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
    
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len,\
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))  
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
            
            if y_ticks_l_r == "off": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len,\
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length= x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
            
                graph.tick_params(axis = "y", which='major', \
                                  direction= 'out', \
                                  left = False, right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len,\
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
            
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction ='out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
       
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour \
                                                  [taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", min_0))
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom.
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
            # Error checking for graph type 5.
            if line_type[taxon] > 4 or \
                line_type[taxon] < 0 and taxon != "Zones":
                print("  ")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in line colour number {taxon} in Input "
                      "file.")
                sys.exit()
                
            if marker_typ_type[taxon] > 6 or \
                marker_typ_type[taxon] < 1  and taxon != "Zones":
                print("  ")
                print(f"\nError in marker type number for {taxon} in Input "
                      "file.")
                sys.exit()
    
            if marker_f_col[taxon] > col_max or \
                marker_f_col[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in marker colour fill number for {taxon} in "
                      " Input file.")
                sys.exit()
    
            if marker_e_col[taxon] > col_max or \
                marker_f_col[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in marker edge colour number for {taxon} in "
                      "Input file.")
                sys.exit()                
    
    ###########################################################################
    ###########################################################################
        # Create plot for taxon to be plotted based on parameter choices if
        # graph type is a scatter plot. Graph type 6.
            
        elif taxon == data_list_1 and plot_type_1 == 6:
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified to any
            # plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
                    
    ###########################################################################
            graph.plot(data_2["Depth"], data_2[taxon], \
                       linewidth = 0, \
                       marker = marker_typ_type_2, \
                       ms = marker_s_size_1, \
                       markeredgecolor = marker_e_col_2, \
                       markerfacecolor = marker_f_col_2, \
                       markeredgewidth = marker_e_w_wid_1)
           
            graph.set_xlim(x_limit_top, x_limit_base)
            
            if y_ticks_l_r == "on":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if x_all_ticks== "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction ='out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))  
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False,
                                      right = False)
                    
                if  x_minor_ticks_on_off =="on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))    
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len)
            
            if y_ticks_l_r == "off": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x",which ='major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len)
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off =="on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False) 
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))      
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
            
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction ='out', labelright = True, \
                                  labelleft = False, rotation = y_lab_rot) 
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour \
                                           (taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour \
                                            (taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)            
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation =y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", min_0))
            
            graph.tick_params(axis = "x" ,labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
            # Error checking for graph type 6.
            if marker_typ_type[taxon] > 6 or \
                marker_typ_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in marker type number for {taxon} in Input "
                      "file.")
                sys.exit() 
                
            if marker_f_col[taxon] > col_max or \
                marker_f_col[taxon]< 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in marker fill colour number for {taxon} in "
                      "Input file.")
                sys.exit()
    
            if marker_e_col[taxon] > col_max or \
                marker_f_col[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nError in marker type edge colour number for {taxon}"
                      " in Input file.")
                sys.exit()                
    
    ###########################################################################
    ###########################################################################
        # Create plot for taxon to be plotted based on parameter choices. If
        # graphtype is one of the two possible stack graphs. Graph type 7.    
            
        elif taxon == data_list_1 and plot_type_1 == 7:
            
    ###########################################################################
            # Alter if percentage has been calculated.
            if num_stack == 1:
                stack_colours_1 = [colour(x) for x in stack_plot_1_colours]
                if stack_calc_1 == "yes":
                    graph.stackplot(data_2["Depth"], stack_1_sums_1_calc, \
                                    stack_1_sums_2_calc, stack_1_sums_3_calc, \
                                    stack_1_sums_4_calc, stack_1_sums_5_calc, \
                                    colors = stack_colours_1)
                    
                graph.stackplot(data_2["Depth"], stack_1_sums_1, \
                                                 stack_1_sums_2, \
                                                 stack_1_sums_3, \
                                                 stack_1_sums_4, \
                                                 stack_1_sums_5, \
                                                 colors = stack_colours_1)
               
            if num_stack == 2:
                stack_colours_2 = [colour(x) for x in stack_plot_2_colours]
                if stack_calc_2 == "yes":
                    graph.stackplot(data_2["Depth"], stack_2_sums_1_calc, \
                                                     stack_2_sums_2_calc, \
                                                     stack_2_sums_3_calc, \
                                                     stack_2_sums_4_calc, \
                                                     stack_2_sums_5_calc, \
                                                     colors = stack_colours_1)
                
                graph.stackplot(data_2["Depth"], stack_2_sums_1, \
                                stack_2_sums_2, stack_2_sums_3, \
                                stack_2_sums_4, stack_2_sums_5, \
                                colors = stack_colours_2)
    
    ###########################################################################
            graph.set_xlim(x_limit_top, x_limit_base)
            
            if y_ticks_l_r == "on":
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                                     [taxon]))  
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                   
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length =x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if  x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                        
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))  
                    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width =  x_major_tick_wid, \
                                  length = x_major_tick_len)
                        
            if y_ticks_l_r == "off": 
                if x_all_ticks == "on":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction = 'out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len, \
                                      color = colour(taxa_x_tick_maj_colour \
                                      [taxon]))
                    
                if x_all_ticks == "off":
                    graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                      direction = 'out', \
                                      labelbottom = False)
                    
                    graph.tick_params(axis = "x", which = 'major', \
                                      direction ='out', bottom = True, \
                                      width = x_major_tick_wid, \
                                      length = x_major_tick_len)
                    
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction ='out', left = False, \
                                      right = False)
                    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
            
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))      
                    
                graph.tick_params(axis = "x", which ='major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
            
            graph.set_xlim(x_limit_top, x_limit_base)
            
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int)) 
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)            
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.set_xlabel(x_title, fontsize = x_title_fontsize, \
                             rotation = x_title_rotation, \
                             color = colour(x_title_text_colour), \
                             weight = bold_on_off(x_title_text_bold))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", min_0)) 
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = True, \
                              rotation = x_lab_rot)
            
            num_stack = num_stack + 1
            
    ###########################################################################
            # Add annotations for rc dates.
            if rc_ages_on_off == "on":
                if rc_age_labels_bold == "on":
                    rc_age_labels_bold = "bold"
                else:
                    rc_age_labels_bold = "normal"
                    
                if rc_age_title_on_off == "on":
                    if rc_age_title_bold == "on":
                        rc_age_title_bold = "bold"
                    else:
                        rc_age_title_bold = "normal" 
                    
                for label,depth in zip(rc_age_labels, rc_age_depths):
                    
                    graph.annotate(label, textcoords = "data", \
                                   xy = (depth, rc_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = rc_age_labels_bold, \
                                   fontsize = rc_age_labels_font_size, \
                                   color = colour(rc_age_labels_colour))
                        
                if rc_age_title_on_off == "on": 
                    graph.annotate(rc_age_title, textcoords = "data", \
                                   xy = (rc_age_title_depth, \
                                   rc_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = rc_age_title_rotation, \
                                   fontsize = rc_age_title_font_size, \
                                   color = colour(rc_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = rc_age_title_bold)
                        
    ###########################################################################
            # Add annotations for int dates. Date line.
            if int_ages_on_off == "on":
                if int_age_labels_bold == "on":
                    int_age_labels_bold = "bold"
                else:
                    int_age_labels_bold = "normal"
                    
                if int_age_title_on_off == "on":
                    if int_age_title_bold == "on":
                        int_age_title_bold = "bold"
                    else:
                        int_age_title_bold = "normal"
                
                for label,depth in zip(int_age_labels, int_age_depths):
                    
                    graph.annotate(label,textcoords = "data", \
                                   xy = (depth, int_age_location_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_labels_rotation, \
                                   ha = "center", va = "center", \
                                   weight = int_age_labels_bold,\
                                   fontsize = int_age_labels_font_size, \
                                   color = colour(int_age_labels_colour))
    
                graph.annotate(int_umd_age, textcoords ="data", \
                               xy = (x_limit_top, int_age_location_offset),\
                               annotation_clip =False, \
                               rotation = int_age_labels_rotation, \
                               ha = "center", va = "center", \
                               weight = int_age_labels_bold, \
                               fontsize = int_age_labels_font_size,\
                               color = colour(int_age_labels_colour))
                    
                if int_age_title_on_off == "on":
                    graph.annotate(int_age_title,textcoords ="data", \
                                   xy = (int_age_title_depth, \
                                   int_age_title_offset), \
                                   annotation_clip = False, \
                                   rotation = int_age_title_rotation, \
                                   fontsize = int_age_title_font_size, \
                                   color = colour(int_age_title_colour), \
                                   ha = "right", va = "center", \
                                   weight = int_age_title_bold)
    
                graph.annotate('', xy = (x_limit_top - int_lines_corr_l, \
                               int_lines_offset), xycoords = 'data', \
                               xytext = (x_limit_base + \
                               int_lines_corr_l, \
                               int_lines_offset), arrowprops = \
                               dict(arrowstyle = "-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)
    
                for depth in int_age_depths:
                    
                    # All depth marker lines except top and bottom.
                    graph.annotate('', xy = (depth, int_lines_offset + 5 + \
                                  int_lines_corr), xycoords= 'data', \
                                  xytext = (depth, int_lines_offset - \
                                  int_lines_depth_length), \
                                  arrowprops = dict(arrowstyle ="-", \
                                  color = colour(int_lines_colour), \
                                  linewidth = int_lines_width), \
                                  annotation_clip = False)
    
                graph.annotate('', xy = (x_limit_top + 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_top + 1, int_lines_offset - \
                               int_lines_depth_length), \
                               arrowprops = dict(arrowstyle ="-", \
                               color = colour(int_lines_colour), \
                               linewidth = int_lines_width), \
                               annotation_clip = False)            
    
                graph.annotate('', xy = (x_limit_base - 1, int_lines_offset + \
                               5 + int_lines_corr), xycoords = 'data', \
                               xytext = (x_limit_base - 1, int_lines_offset - \
                               int_lines_depth_length), arrowprops = \
                               dict(arrowstyle = "-", color = \
                               colour(int_lines_colour), linewidth = \
                               int_lines_width), annotation_clip = False)
                
    ###########################################################################
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices if graph type is a bar plot. Graph type 1. 
        elif plot_type_1 == 1 and taxon != data_list_1:
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified to any
            # plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
                    
    ###########################################################################
            markerline, stemlines, baseline = graph.stem(data_2["Depth"], \
                                              data_2[taxon], \
                                              linefmt = bar_col_type_2, \
                                              markerfmt = "", \
                                              basefmt="black", \
                                              use_line_collection = True, \
                                              bottom = min_0)   
    
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
    
            if y_ticks_l_r =="on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                      graph.tick_params(axis = "y", which = 'minor', \
                                        direction = 'out', left = False, \
                                        right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)            
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
                
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                        
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction='out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
                                
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
                
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
            
            plt.setp(stemlines, color= bar_col_type_2, \
                     linewidth = bar_wid_g1_1)
            plt.setp(markerline, linewidth = 0, color = "black")
            plt.setp(baseline, linewidth = 0, color = "black") 
                
            graph.spines['top'].set_visible(False)
    
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
    
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(('data', 0))
    
    ###########################################################################
            # Error checking for bar graph type 1.
            if bar_col_type[taxon] > col_max or \
                bar_col_type[taxon] < 1 and taxon != "Zones":
                print("  ")
                print(f"\nBar colour number designation for {taxon} in "
                      f"Input file is out of range (1 - {col_max}).")
                sys.exit()
                
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices if graph type is line plot with depth bars. Graph type 2.
        elif plot_type_1 == 2 and taxon != data_list_1: 
    
    ###########################################################################
            # Adjustments required if exaggeration has been specified.
            if taxa_exag_type[taxon] == 3:
                if taxa_exag_line_col[taxon] not in range (1, col_max) or \
                    taxa_exag_ls[taxon] not in range (1, 4):
                    print("  ")
                    print (f"\nExaggeration aesthetics in Input file are "
                           f"out of bounds for {taxon}.")
                    sys.exit() 
                    
                graph.plot(data_2["Depth"], data_2[taxon] * taxa_exag[taxon], \
                                color = colour(taxa_exag_line_col[taxon]), \
                                linewidth = taxa_exag_lw[taxon], \
                                linestyle = line_styles(taxa_exag_ls[taxon]))
                    
                graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                           decimal =-1))   
                #graph.set_ylim(0, data_2[taxon].max())
                
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))       
                        
            if taxa_exag_type[taxon] == 4:
                if taxa_exag_col[taxon] not in range (1, col_max) or \
                   taxa_exag_line_col[taxon] not in range (1, col_max) \
                   or taxa_exag_ls[taxon] not in range (1, 4) or \
                   taxa_exag_trans[taxon] * 100 not in range (0, 100):
                    print("  ")                    
                    print (f"\nExaggeration aesthetics are out of bounds for "
                           f"{taxon} in Input file.")
                    sys.exit()                  
                    
                graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                   taxa_exag[taxon], \
                                   color = colour(taxa_exag_col[taxon]), \
                                   linewidth = taxa_exag_lw[taxon], \
                                   alpha = taxa_exag_trans[taxon])
                    
                graph.plot(data_2["Depth"], data_2[taxon] * \
                           taxa_exag[taxon], \
                           color = colour(taxa_exag_line_col[taxon]), \
                           linewidth = taxa_exag_lw[taxon], \
                           linestyle = line_styles(taxa_exag_ls[taxon]))
                
                graph.set_ylim(0, new_max_taxa_dict[taxon]) 
    
                if data_2[taxon].max() < 10:
                    graph.set_ylim(0, yu_lim + 20)
                else:
                    graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))  
    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = fill_colour_type_2, \
                               linewidth = line_width_1, \
                               alpha = fill_trans_type_1)
                
            markerline, stemlines, baseline = graph.stem(data_2["Depth"], \
                                              data_2[taxon], \
                                              linefmt = bar_col_type_2, \
                                              markerfmt = "", \
                                              basefmt = "black", \
                                              use_line_collection = True, \
                                              bottom = min_0)
                
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color = line_colour_type_2, \
                       linewidth = line_width_1, linestyle = line_type_2)
           
            graph.set_xlim(x_limit_top, x_limit_base)
    
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
            
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)            
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False) 
    
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len,\
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction='out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction='out', labelright =True, \
                              labelleft = False, rotation = y_lab_rot) 
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
    
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
    
            plt.setp(stemlines, color= bar_col_type_2, linewidth = bar_wid_1)
            plt.setp(markerline, linewidth = 0, color = "black")
            plt.setp(baseline, linewidth = 0, color = "black") 
                
            graph.spines['top'].set_visible(False)
    
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.0, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.yaxis.labelpad = y_lab_gap
            graph.spines['bottom'].set_position(("data", 0)) 
    
            # Error checking.
            if bar_col_type[taxon] > col_max or \
                bar_col_type[taxon] < 1 and taxon != "Zones":
                print("")
                print(f"\nBar colour number designation for {taxon} in Input "
                      f"file is out of range (1 - {col_max}).")
                sys.exit()
    
            if line_type[taxon] > 4 or \
                line_type[taxon] < 1 and taxon != "Zones":
                print("")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
    
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1  and taxon != "Zones":
                print("")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit()
    
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices if graph type is line plot. Graph type 3.
        elif plot_type_1 == 3 and taxon != data_list_1: 
                  
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color = line_colour_type_2, \
                       linewidth = line_width_1, linestyle = line_type_2)
    
    ###########################################################################
            # Adjustments required if exaggeration has been specified.
            if taxa_exag[taxon] > 0 and pd.isnull(taxa_exag[taxon]) == False:
                if taxa_exag_type[taxon] == 3:
                    if taxa_exag_line_col[taxon] not in range (1, col_max) \
                        or taxa_exag_ls[taxon] not in range (1, 4):
                        print("  ")                    
                        print (f"\nExaggeration aesthetics are out of bounds"
                               f" for {taxon} in Input file.")
                        sys.exit()
    
                    graph.plot(data_2["Depth"], data_2[taxon] * \
                               taxa_exag[taxon], \
                               color = colour(taxa_exag_line_col[taxon]), \
                               linewidth = taxa_exag_lw[taxon], \
                               linestyle = line_styles(taxa_exag_ls[taxon]))
    
                    graph.set_ylim(0, data_2[taxon].max())
    
                    if data_2[taxon].max() < 10:
                        graph.set_ylim(0, yu_lim + 20)
                    else:
                        graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1)) 
                        
                if taxa_exag_type[taxon] == 4:
                    if taxa_exag_col[taxon] not in range (1, col_max) or \
                        taxa_exag_line_col[taxon] not in range (1, col_max) \
                        or taxa_exag_ls[taxon] not in range (1, 4) or \
                        taxa_exag_trans[taxon] * 100 not in range (0, 100):
                        print("  ")                    
                        print (f"\nExaggeration aesthetics are out of bounds"
                               f" for {taxon} in Input file.")
                        sys.exit() 
                        
                    graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                       taxa_exag[taxon], \
                                       color = colour(taxa_exag_col[taxon]), \
                                       linewidth = taxa_exag_lw[taxon], \
                                       alpha = taxa_exag_trans[taxon])
                        
                    graph.plot(data_2["Depth"],data_2[taxon] * \
                               taxa_exag[taxon], \
                               color = colour(taxa_exag_line_col[taxon]), \
                               linewidth = taxa_exag_lw[taxon], \
                               linestyle = line_styles(taxa_exag_ls[taxon]))
                        
                    graph.set_ylim(0, data_2[taxon].max())
                    
                    if data_2[taxon].max() < 10:
                        graph.set_ylim(0, yu_lim + 20)
                    else:
                        graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1)) 
                    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = "white", linewidth = 0, alpha = 1)
            
            if extra_yn != "none":
                for x in data_list_extra:
                    if taxon in x:
                        graph.plot(data_extra_2["Depth"], data_extra_2[x], \
                                   color = colour(line_colour_type_ex[x]), \
                                   linewidth = line_width_type_ex[x], \
                                   linestyle = line_styles(line_type_ex[x]))
                            
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
    
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len,\
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, \
                                  width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False,\
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)           
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction='out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
    
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright =True, \
                              labelleft = False, rotation = y_lab_rot) 
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
    
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
    
            graph.yaxis.labelpad = y_lab_gap
    
    ###########################################################################
            # Make adjustments if this is a NON STD SCALING plot.
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_1))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_2))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_3))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] == "mini":
                
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_4))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_5))
                    
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[0])))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[1])))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[2])))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[3])))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[4])))
                
            if taxon == non_std_scaling_1 and \
                non_std_spine_on_off_1 == "off":
                graph.spines['bottom'].set_visible(False)
            if taxon == non_std_scaling_2 and non_std_spine_on_off_2 == "off":
                graph.spines['bottom'].set_visible(False)
            if taxon == non_std_scaling_3 and non_std_spine_on_off_3 == "off":
                graph.spines['bottom'].set_visible(False)
            if taxon == non_std_scaling_4 and non_std_spine_on_off_4 == "off":
                graph.spines['bottom'].set_visible(False)
            if taxon == non_std_scaling_5 and non_std_spine_on_off_5 == "off":
                graph.spines['bottom'].set_visible(False) 
                
    ###########################################################################
            # Error checking for graph type 2.
            if line_type[taxon] > 4 or line_type[taxon] < 1 \
                and taxon != "Zones":
                print("")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit() 
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1 and taxon != "Zones":
                print("")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit() 
    
    ###########################################################################
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices if graph type is a line plot with solid shading underneath. 
        # Graph type 4.
    
        elif plot_type_1 == 4 and taxon != data_list_1:
    ###########################################################################
            # Adjustments required if exaggeration has been specified.
            if taxa_exag[taxon] > 0 and pd.isnull(taxa_exag[taxon]) == False:
                if taxa_exag_type[taxon] == 3:
                    if taxa_exag_line_col[taxon] not in range (1, col_max) \
                        or taxa_exag_ls[taxon] not in range (1, 4):
                        print("  ")
                        print (f"\nExaggeration aesthetics out of bounds for "
                               f"{taxon} in Input file.")
                        sys.exit()
                    
                    graph.plot(data_2["Depth"], data_2[taxon] * \
                               taxa_exag[taxon], \
                               color = colour(taxa_exag_line_col[taxon]), \
                               linewidth = taxa_exag_lw[taxon], \
                               linestyle = line_styles(taxa_exag_ls[taxon]))
                        
                    graph.set_ylim(0, data_2[taxon].max())
    
                    if data_2[taxon].max() < 10:
                        graph.set_ylim(0, yu_lim + 20)
                    else:
                        graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))
        
                if taxa_exag_type[taxon] == 4:
                    if taxa_exag_col[taxon] not in range (1, col_max) \
                        or taxa_exag_line_col[taxon] \
                        not in range (1, col_max) or taxa_exag_ls[taxon] \
                        not in range (1, 4) or \
                        taxa_exag_trans[taxon] * 100 not in range (0, 100):
                        print("  ")
                        print (f"\nExaggeration aesthetics out of bounds for "
                               f"{taxon} in Input file.")
                        sys.exit() 
                        
                    graph.fill_between(data_2["Depth"], data_2[taxon] * \
                                       taxa_exag[taxon], \
                                       color = colour(taxa_exag_col[taxon]), \
                                       linewidth = taxa_exag_lw[taxon], \
                                       alpha = taxa_exag_trans[taxon])
                        
                    graph.plot(data_2["Depth"], data_2[taxon] * \
                               taxa_exag[taxon], \
                               color = colour(taxa_exag_line_col[taxon]),\
                               linewidth = taxa_exag_lw[taxon], \
                               linestyle = line_styles(taxa_exag_ls[taxon]))
                        
                    graph.set_ylim(0, data_2[taxon].max())
                    
                    if data_2[taxon].max() < 10:
                        graph.set_ylim(0, yu_lim + 20)
                    else:
                        graph.set_ylim(0, np.round(new_max_taxa_dict[taxon], \
                                               decimals =-1))
                    
    ###########################################################################
            graph.fill_between(data_2["Depth"], data_2[taxon], \
                               color = fill_colour_type_2, \
                               linewidth = line_width_1, \
                               alpha = fill_trans_type_1)
                
            graph.plot(data_2["Depth"], data_2[taxon], \
                       color = line_colour_type_2, \
                       linewidth = line_width_1, linestyle = line_type_2)
            
            graph.set_xlim(x_limit_top, x_limit_base) 
            
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
    
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
            
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
    
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                                 [taxon]))
                
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
    
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction ='out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
            
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom =False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot)
    
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
    
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.2, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.yaxis.labelpad = y_lab_gap
    
    ###########################################################################
            # Adjustments if plot is NON STD SCALING.
            if taxon == non_std_scaling_1 and \
               non_std_spine_start_list[0] == "mini":
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_1))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_2))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_3))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] == "mini":
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_4))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_5))
                
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[0])))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[1])))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[2])))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[3])))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[4])))
                
            if taxon == non_std_scaling_1 and non_std_spine_on_off_1 == "off":
                graph.spines['bottom'].set_visible(False)
    
            if taxon == non_std_scaling_2 and non_std_spine_on_off_2 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_3 and non_std_spine_on_off_3 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_4 and non_std_spine_on_off_4 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_5 and non_std_spine_on_off_5 == "off":
                graph.spines['bottom'].set_visible(False) 
                
    ###########################################################################
            # Error checking for graph type 4.
            if line_type[taxon] > 4 or line_type[taxon] < 1 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
        
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1 and taxon != "Zones":
                print(" ")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if fill_colour_type[taxon] > col_max or \
                fill_colour_type[taxon] < 1 and taxon != "Zones":
                print(" ")
                print(f"\nError in fill colour number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if fill_trans_type[taxon] > 1 or fill_trans_type[taxon] < 0 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in fill colour transparency for {taxon} in "
                      "Input file.")
                sys.exit()
    
    ###########################################################################
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices if graph type is a line and marker plot. 
        # Graph type 5. 
        elif plot_type_1 == 5 and taxon != data_list_1: 
            
    ###########################################################################
            # Adjustments required if exaggeration has been specified to any
            # plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
    
    ###########################################################################
            graph.plot(data_2["Depth"], data_2[taxon], color = \
                       line_colour_type_2, linewidth = line_width_1, \
                       linestyle = line_type_2, marker =marker_typ_type_2, \
                       ms = marker_s_size_1, \
                       markeredgecolor = marker_e_col_2, \
                       markerfacecolor = marker_f_col_2, \
                       markeredgewidth = marker_e_w_wid_1)
                
            if extra_yn != "none":
                for x in data_list_extra:
                    
                    if taxon in x:
                        graph.plot(data_extra["Depth"], data_extra[x], \
                                   color = colour(line_colour_type_ex[x]), \
                                   linewidth = line_width_type_ex[x], \
                                   linestyle = line_styles(line_type_ex[x]), \
                                   marker = marker_type(marker_typ_type_ex[x]), \
                                   ms = marker_s_size_ex[x], \
                                   markeredgecolor = colour(marker_e_col_ex[x]), \
                                   markerfacecolor = colour(marker_f_col_ex[x]), \
                                   markeredgewidth = marker_e_w_wid_ex[x])
            
            graph.set_xlim(x_limit_top, x_limit_base) 
    
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
            
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                                     [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y",which ='minor', \
                                      direction = 'out', left = False, \
                                      right = False)           
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
                
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                                     [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
                    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction ='out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction='out', labelright =True, \
                              labelleft = False, rotation = y_lab_rot) 
                
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour \
                                           (taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
    
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.0, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.yaxis.labelpad = y_lab_gap
    
    ###########################################################################
            # Adjustments if this plot is NON STANDARD SCALING.
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] == "mini":
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_1))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_2))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] == "mini":
                
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_3))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] == "mini":
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_4))
               
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_5))
                
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[0])))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[1])))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[2])))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[3])))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[4])))
                
            if taxon == non_std_scaling_1 and non_std_spine_on_off_1 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_2 and non_std_spine_on_off_2 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_3 and non_std_spine_on_off_3 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_4 and non_std_spine_on_off_4 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_5 and non_std_spine_on_off_5 == "off":
                graph.spines['bottom'].set_visible(False) 
                
    ###########################################################################
            # Error checking for graph type 5.
            if line_type[taxon] > 4 or line_type[taxon] < 1 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in line type number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if  line_colour_type[taxon] > col_max or \
                line_colour_type[taxon] < 1 and taxon != "Zones":
                print(" ")
                print(f"\nError in line colour number for {taxon} in Input "
                      "file.")
                sys.exit()
                
            if marker_typ_type[taxon] > 6 or marker_typ_type[taxon] < 1 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in marker type number for {taxon} in Input "
                      "file.")
                sys.exit() 
    
            if marker_f_col[taxon] > col_max or marker_f_col[taxon] < 1 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in marker type colour fill number for {taxon}"
                      " in Input file.")
                sys.exit()
    
            if marker_e_col[taxon] > col_max or marker_e_col[taxon] < 1 \
                and taxon != "Zones":
                print("")
                print(f"\nError in marker type edge colour number for"
                      f" {taxon} in Input file.")
                sys.exit()
    
    ###########################################################################
        # Create plot for taxon (not first) to be plotted based on parameter 
        # choices. If graph type is a scatterplot. Graph type 6.
        elif plot_type_1 == 6 and taxon != data_list_1: 

    ###########################################################################
            # Adjustments required if exaggeration has been specified to any
            # plot.
            # if exag["exag"].max() > 0: 
            #     if data_2[taxon].max() < 10:
            #         graph.set_ylim(0, yu_lim + 20)
            #     else:
            #         graph.set_ylim(0, yu_lim)
                    
    ###########################################################################
            graph.plot(data_2["Depth"], data_2[taxon], linewidth = 0, \
                            marker = marker_typ_type_2, \
                            ms = marker_s_size_1, \
                            markeredgecolor = marker_e_col_2, \
                            markerfacecolor = marker_f_col_2, \
                            markeredgewidth = marker_e_w_wid_1)
                
            if extra_yn != "none":
                for x in data_list_extra:
                    
                    if taxon in x:
                        graph.plot(data_extra["Depth"], data_extra[x], \
                                   linewidth = 0, \
                                   marker = marker_type(marker_typ_type_ex[x]), \
                                   ms = marker_s_size_ex[x], \
                                   markeredgecolor = colour(marker_e_col_ex[x]), \
                                   markerfacecolor = colour(marker_f_col_ex[x]), \
                                   markeredgewidth = marker_e_w_wid_ex[x])
            
            graph.set_xlim(x_limit_top, x_limit_base) 
    
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
            
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which ='major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)            
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
                
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which ='minor', \
                                      direction = 'out', bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x", which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
                    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction = 'out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
                
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.0, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.yaxis.labelpad = y_lab_gap
            
    ###########################################################################
            # Make adjustments if this is NON STD SCALING plot.
            if taxon == non_std_scaling_1 and \
               non_std_spine_start_list[0] == "mini":
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_1))
            elif taxon == non_std_scaling_2 and \
                 non_std_spine_start_list[1] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_2))
            elif taxon == non_std_scaling_3 and \
                 non_std_spine_start_list[2] == "mini":
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_3))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] == "mini":
                
               graph.spines['bottom'].set_position(("data", \
                                                    non_std_scaling_y_min_4))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] == "mini":
                
                graph.spines['bottom'].set_position(("data", \
                                                     non_std_scaling_y_min_5))
                
            if taxon == non_std_scaling_1 and \
                non_std_spine_start_list[0] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[0])))
            elif taxon == non_std_scaling_2 and \
                non_std_spine_start_list[1] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[1])))
            elif taxon == non_std_scaling_3 and \
                non_std_spine_start_list[2] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[2])))
            elif taxon == non_std_scaling_4 and \
                non_std_spine_start_list[3] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[3])))
            elif taxon == non_std_scaling_5 and \
                non_std_spine_start_list[4] != "mini":
                graph.spines['bottom'].set_position \
                    (("data", float(non_std_spine_start_list[4])))
                
            if taxon == non_std_scaling_1 and \
                non_std_spine_on_off_1 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_2 and \
                non_std_spine_on_off_2 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_3 and non_std_spine_on_off_3 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_4 and non_std_spine_on_off_4 == "off":
                graph.spines['bottom'].set_visible(False)
                
            if taxon == non_std_scaling_5 and non_std_spine_on_off_5 == "off":
                graph.spines['bottom'].set_visible(False) 
                
    ###########################################################################
            # Error checking for graph type 6.
            if marker_typ_type[taxon] > 6 or marker_typ_type[taxon] < 1 \
                and taxon != "Zones":
                print(" ")
                print(f"\nError in arker type number for {taxon} in Input "
                      "file.")
                sys.exit() 
                
            if marker_f_col[taxon] > col_max or marker_f_col[taxon] <1 \
                and taxon != "Zones":
                print("")
                print(f"\nError in marker type fill colour number for {taxon}"
                      " in Input file.")
                sys.exit()
    
            if marker_e_col[taxon] > col_max or marker_f_col[taxon] < 1 \
                and taxon != "Zones":
                print("")        
                print(f"\nError in marker type edge colour number for {taxon}"
                      " in Input file.")
                sys.exit() 
                
    ###########################################################################
    ###########################################################################
    # Stack plots, two are allowed at present but this can be expanded if 
    # required. Graph type 7
        elif plot_type_1 == 7  and taxon != data_list_1:
            
    ###########################################################################
            # Adjust if percentage has been calculated.
            if num_stack == 1:
                if num_stack_plots == 1 or num_stack_plots == 2:
                    stack_colours_1 = [colour(x) for x in stack_plot_1_colours]
                    
                    if stack_calc_1 == "yes":
                        stack_line_atts = []
                        stack_line_atts.append(stack_plot_1_line_colour)
                        stack_line_atts.append(stack_plot_1_lw)
                        
                        if any(i > 0 for i in stack_line_atts):
                            
                            stack_2 =[x + y for x, y in zip(stack_1_sums_1, \
                                                           stack_1_sums_2)]
                            stack_3 =[x + y + z for x, y, z in \
                                      zip(stack_1_sums_1, stack_1_sums_2, \
                                      stack_1_sums_3)]
                            stack_4 =[x + y + z + a for x, y, z, a in \
                                     zip(stack_1_sums_1, stack_1_sums_2, \
                                     stack_1_sums_3, stack_1_sums_4)]
                                
                            stack_5 =[x + y + z + a + b for x ,y ,z, a, b \
                                     in zip(stack_1_sums_1, stack_1_sums_2, \
                                     stack_1_sums_3, stack_1_sums_4, \
                                     stack_1_sums_5)]
                            
                            graph.stackplot(data_2["Depth"], \
                                            stack_1_sums_1_calc, \
                                            stack_1_sums_2_calc, \
                                            stack_1_sums_3_calc, \
                                            stack_1_sums_4_calc, \
                                            stack_1_sums_5_calc, \
                                            colors = stack_colours_1)
                                
                            graph.plot(data_2["Depth"], stack_1_sums_1_calc, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                            graph.plot(data_2["Depth"], [u + v for u,v in  \
                                       zip(stack_1_sums_1_calc, \
                                       stack_1_sums_2_calc)], \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w for u,v,w \
                                       in zip(stack_1_sums_1_calc, \
                                              stack_1_sums_2_calc, \
                                              stack_1_sums_3_calc)], \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w + x for \
                                       u,v,w,x in zip(stack_1_sums_1_calc, \
                                                      stack_1_sums_2_calc, \
                                                      stack_1_sums_3_calc, \
                                                      stack_1_sums_4_calc)], \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w + x + y \
                                       for u,v,w,x,y in \
                                       zip(stack_1_sums_1_calc, \
                                           stack_1_sums_2_calc, \
                                           stack_1_sums_3_calc, \
                                           stack_1_sums_4_calc, \
                                           stack_1_sums_5_calc)], \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                        else:
                            graph.stackplot(data_2["Depth"], \
                                            stack_1_sums_1_calc, \
                                            stack_1_sums_2_calc, \
                                            stack_1_sums_3_calc, \
                                            stack_1_sums_4_calc, \
                                            stack_1_sums_5_calc, \
                                            colors = stack_colours_1)
    
                                
                    if stack_calc_1 == "no" or pd.isnull(stack_calc_1) == True:
                        stack_line_atts = []
                        stack_line_atts.append(stack_plot_1_line_colour)
                        stack_line_atts.append(stack_plot_1_lw)
                        
                        if any(i > 0 for i in stack_line_atts):
                            stack_2 = [x + y for x, y in zip(stack_1_sums_1, \
                                                             stack_1_sums_2)]
                            stack_3 = [x + y + z for x, y, z \
                                       in zip(stack_1_sums_1, \
                                              stack_1_sums_2, \
                                              stack_1_sums_3)]
                            stack_4 = [x + y + z + a for x, y, z, a \
                                     in zip(stack_1_sums_1, \
                                            stack_1_sums_2, \
                                            stack_1_sums_3, \
                                            stack_1_sums_4)]
                            stack_5 = [x + y + z + a + b for x, y, z, a, b \
                                     in zip(stack_1_sums_1, \
                                            stack_1_sums_2, \
                                            stack_1_sums_3, \
                                            stack_1_sums_4, \
                                            stack_1_sums_5)]
        
                            graph.stackplot(data_2["Depth"], stack_1_sums_1, \
                                                             stack_1_sums_2, \
                                                             stack_1_sums_3, \
                                                             stack_1_sums_4, \
                                                             stack_1_sums_5, \
                                            colors = stack_colours_1)
        
                            graph.plot(data_2["Depth"],stack_1_sums_1, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_2, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_3, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_4, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                            
                            graph.plot(data_2["Depth"], stack_5, \
                                       linewidth = stack_plot_1_lw, \
                                       color = colour(stack_plot_1_line_colour))
                        else:
                            graph.stackplot(data_2["Depth"],stack_1_sums_1, \
                                                            stack_1_sums_2, \
                                                            stack_1_sums_3, \
                                                            stack_1_sums_4, \
                                                            stack_1_sums_5, \
                                            colors = stack_colours_1)
                   
            if num_stack == 2:
                if num_stack_plots == 2:
                    stack_colours_2 = [colour(x) for x in stack_plot_2_colours]
                    
                    if stack_calc_2 == "yes":
                        stack_line_atts = []
                        stack_line_atts.append(stack_plot_2_line_colour)
                        stack_line_atts.append(stack_plot_2_lw)
                        
                        if any(i > 0 for i in stack_line_atts):
                            
                            stack_2 =[x + y for x, y in zip(stack_2_sums_1, \
                                                            stack_2_sums_2)]
                            stack_3 =[x + y + z for x, y, z \
                                      in zip(stack_2_sums_1, stack_2_sums_2, \
                                             stack_2_sums_3)]
                            stack_4 =[x + y + z + a for x, y, z, a \
                                     in zip(stack_2_sums_2, stack_2_sums_2, \
                                            stack_2_sums_3, stack_2_sums_4)]
                                
                            stack_5 =[x + y + z + a + b for x ,y ,z, a, b \
                                     in zip(stack_2_sums_1, stack_2_sums_2, \
                                            stack_2_sums_3, stack_2_sums_4, \
                                            stack_2_sums_5)]
                            
                            graph.stackplot(data_2["Depth"], \
                                            stack_2_sums_1_calc, \
                                            stack_2_sums_2_calc, \
                                            stack_2_sums_3_calc, \
                                            stack_2_sums_4_calc, \
                                            stack_2_sums_5_calc, \
                                            colors = stack_colours_2)
                                
                            graph.plot(data_2["Depth"], stack_2_sums_1_calc, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                            graph.plot(data_2["Depth"], [u + v for u,v in  \
                                       zip(stack_2_sums_1_calc, \
                                       stack_2_sums_2_calc)], \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w for \
                                       u,v,w in zip(stack_2_sums_1_calc,
                                                    stack_2_sums_2_calc, \
                                                    stack_2_sums_3_calc)], \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w + x for \
                                       u,v,w,x in zip(stack_2_sums_1_calc, \
                                                      stack_2_sums_2_calc, \
                                                      stack_2_sums_3_calc, \
                                                      stack_2_sums_4_calc)], \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                            graph.plot(data_2["Depth"], [u + v + w + x + y \
                                       for u,v,w,x,y in \
                                       zip(stack_2_sums_1_calc, \
                                           stack_2_sums_2_calc, \
                                           stack_2_sums_3_calc, \
                                           stack_2_sums_4_calc, \
                                           stack_2_sums_5_calc)], \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                        else:
                            graph.stackplot(data_2["Depth"], \
                                            stack_2_sums_1_calc, \
                                            stack_2_sums_2_calc, \
                                            stack_2_sums_3_calc, \
                                            stack_2_sums_4_calc, \
                                            stack_2_sums_5_calc, \
                                            colors = stack_colours_2)
                                
                    if stack_calc_2 == "no" or pd.isnull(stack_calc_2) == True:
                        stack_line_atts = []
                        stack_line_atts.append(stack_plot_2_line_colour)
                        stack_line_atts.append(stack_plot_2_lw)
                        
                        if any(i > 0 for i in stack_line_atts):
                            stack_2 = [x + y for x, y in zip(stack_2_sums_1, \
                                                           stack_2_sums_2)]
                            stack_3 = [x + y + z for x, y, z \
                                       in zip(stack_2_sums_1, stack_2_sums_2, \
                                              stack_2_sums_3)]
                            stack_4 = [x + y + z + a for x, y, z, a \
                                     in zip(stack_2_sums_1, stack_2_sums_2, \
                                            stack_2_sums_3, stack_2_sums_4)]
                            stack_5 = [x + y + z + a + b for x, y, z, a, b \
                                     in zip(stack_2_sums_1, stack_2_sums_2, \
                                            stack_2_sums_3, stack_2_sums_4, \
                                            stack_2_sums_5)]
        
                            graph.stackplot(data_2["Depth"], stack_2_sums_1, \
                                            stack_2_sums_2, stack_2_sums_3, \
                                            stack_2_sums_4, stack_2_sums_5, \
                                            colors = stack_colours_2)
        
                            graph.plot(data_2["Depth"],stack_2_sums_1, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_2, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_3, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                                
                            graph.plot(data_2["Depth"], stack_4, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                            
                            graph.plot(data_2["Depth"], stack_5, \
                                       linewidth = stack_plot_2_lw, \
                                       color = colour(stack_plot_2_line_colour))
                        else:
                            graph.stackplot(data_2["Depth"],stack_2_sums_1, \
                                            stack_2_sums_2, stack_2_sums_3, \
                                            stack_2_sums_4, stack_2_sums_5, \
                                            colors = stack_colours_2)
    
    ###########################################################################
            graph.set_xlim(x_limit_top, x_limit_base)
            graph.set_ylim(0, 100) 
    
            graph.xaxis.set_major_locator(ticker.MultipleLocator(x_major_int))
            graph.yaxis.set_major_locator(ticker.MultipleLocator(y_major_int))
                
            if y_ticks_l_r == "on":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out', left = True, \
                                  right = True, width = y_major_tick_wid, \
                                  length= y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon])) 
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = True, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)
                    
            if y_ticks_l_r == "off":
                graph.tick_params(axis = "y", which = 'major', \
                                  direction = 'out' , left = False, \
                                  right = True, width = y_major_tick_wid, \
                                  length = y_major_tick_len, \
                                  color = colour(taxa_y_tick_maj_colour \
                                  [taxon]))
                
                if y_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = True, \
                                      width = y_minor_tick_wid, \
                                      length = y_minor_tick_len, \
                                      color = colour(taxa_y_tick_min_colour \
                                      [taxon]))
                        
                    graph.yaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (y_minor_int))
                    
                if y_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "y", which = 'minor', \
                                      direction = 'out', left = False, \
                                      right = False)            
    
            if x_all_ticks == "off":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction='out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction = 'out', bottom = True, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))
                
                if x_minor_ticks_on_off == "on":
                    graph.tick_params(axis = "x", which ='minor', \
                                      direction = 'out' , bottom = True, \
                                      width = x_minor_tick_wid, \
                                      length = x_minor_tick_len, \
                                      color = colour(taxa_x_tick_min_colour \
                                      [taxon]))
                        
                    graph.xaxis.set_minor_locator(ticker.MultipleLocator \
                                                  (x_minor_int))
                    
                if x_minor_ticks_on_off == "off":
                    graph.tick_params(axis = "x",which = 'minor', \
                                      direction = 'out', bottom = False)
                            
            if x_all_ticks == "on":
                graph.tick_params(axis = "x", labelsize = x_lab_font, \
                                  direction = 'out', labelbottom = False)
                
                graph.tick_params(axis = "x", which = 'major', \
                                  direction ='out', bottom = False, \
                                  width = x_major_tick_wid, \
                                  length = x_major_tick_len, \
                                  color = colour(taxa_x_tick_maj_colour \
                                  [taxon]))            
                    
                graph.tick_params(axis = "x", which = 'minor', \
                                  direction = 'out', bottom = False, \
                                  width = x_minor_tick_wid, \
                                  length= x_minor_tick_len, \
                                  color = colour(taxa_x_tick_min_colour \
                                  [taxon]))
                    
            graph.tick_params(axis = "x", labelsize = x_lab_font, \
                              direction ='out', labelbottom = False, \
                              rotation = x_lab_rot)
    
            graph.tick_params(axis = "y", labelsize = y_lab_font, \
                              direction = 'out', labelright = True, \
                              labelleft = False, rotation = y_lab_rot) 
                
            graph.spines['bottom'].set_linestyle(line_styles \
                                                 (taxa_plot_vstyle[taxon]))
            graph.spines['bottom'].set_linewidth(taxa_plot_vs_width[taxon])
            graph.spines['bottom'].set_color(colour \
                                             (taxa_plot_vs_colour[taxon]))
            
            graph.spines['left'].set_linestyle(line_styles \
                                               (taxa_plot_lstyle[taxon]))
            graph.spines['left'].set_linewidth(taxa_plot_ls_width[taxon])
            graph.spines['left'].set_color(colour(taxa_plot_ls_colour[taxon]))
            
            graph.spines['right'].set_linestyle(line_styles \
                                                (taxa_plot_rstyle[taxon]))
            graph.spines['right'].set_linewidth(taxa_plot_rs_width[taxon])
            graph.spines['right'].set_color(colour(taxa_plot_rs_colour[taxon]))
                
            graph.spines['top'].set_visible(False)
            
            graph.set_ylabel(taxon, fontsize = y_title_fontsize, \
                             rotation = y_title_rotation, \
                             verticalalignment = 'bottom', y = 0.0, \
                             ha = "left", \
                             weight = bold_on_off(taxa_taxon_b_bold[taxon]), \
                             color = colour(taxa_taxon_c_col[taxon]))
                
            graph.yaxis.labelpad = y_lab_gap
    
            num_stack = num_stack + 1
    
        fig.align_ylabels(ax_list) 
    
        print(f"\n **Plotting {taxon}**")
    
    ###########################################################################
    ###########################################################################
    # Add in zones to desired depths.
    if zones_on_off == "on":
        zone_lines = zone_lines[1:-1]
        
        for zone, zone_col, zone_style, zone_line_w in \
            zip(zone_lines, zone_line_colour, zone_line_style, \
            zone_line_width):
            
            xy1 = (zone, min_list_round[0])
            xy2 = (zone, 1)
            
            con = ConnectionPatch(xyA = xy1, xyB = xy2, coordsA = "data", \
                                  coordsB = "data", axesA = ax_list[-1], \
                                  axesB = ax_list[0], \
                                  color = colour(zone_col), \
                                  linestyle = line_styles(zone_style), \
                                  linewidth = zone_line_w) 
                
            fig.add_artist(con)
    
    ###########################################################################
    ###########################################################################
    # Add footer and overall title.
    if title_text_on_off == "on":
        
        if title_text_bold == "on":
            title_text_bold = "bold"
        else:
            title_text_bold = "normal"
            
        fig.text(title_x_pos, title_y_pos, title_text, \
                 fontsize = title_font_size, \
                 rotation = title_rotation, \
                 color = colour(title_text_colour), \
                 weight = title_text_bold)
        
    if footer_text_on_off == "on":
        
        if footer_text_bold == "on":
            footer_text_bold = "bold"
        else:
             footer_text_bold = "normal"    
        
        fig.text(footer_x_pos, footer_y_pos, footer_text, \
                 fontsize = footer_font_size, \
                 rotation = footer_rotation, \
                 color = colour( footer_text_colour), \
                 weight = footer_text_bold)
    
    ###########################################################################
    ###########################################################################
    # Add grouping annotations. Up to 10 are allowed at present. Should be
    # ample.
    group_line_dict = {k: v for k, v in zip(group_list, group_lw)}
    group_corr_dict = {k: v for k, v in zip(group_list, group_corr)}
    group_corr_line_dict = {k: v for k, v in zip(group_list, group_corr_line)}
    
    factor = 0.9
    factor_2 = 1
    
    if group_anno_1 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
        taxon_1_1 = group_anno_1_start
        
        group_dict[taxon_1_1].\
            annotate('', xy = (group_anno_1_line_x_offset_start, \
            group_anno_1_line_y_offset_start + \
            group_corr_line_dict["G1"]), \
            xycoords = 'data', \
            xytext = (group_anno_1_line_x_offset_end, \
            group_anno_1_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_1_line_colour), \
            linewidth = group_anno_1_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_1_1]. \
            annotate(group_anno_1_title,textcoords = "data", \
            xy = (group_anno_1_line_x_offset_start - 5, \
            (group_anno_1_line_y_offset_start + \
            (group_anno_1_line_y_offset_end \
             - group_anno_1_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, ha = "center", \
            va = "top", \
            weight = bold_on_off(group_anno_1_title_bold), \
            fontsize =group_anno_1_title_font_size, \
            color = colour(group_anno_1_title_colour ))
            
        group_dict[taxon_1_1]. \
            annotate('', xy = (group_anno_1_line_x_tag_end, \
            group_anno_1_line_y_tag_end), \
            xycoords = 'data', \
            xytext = (group_anno_1_line_x_offset_start - \
            group_corr_dict["G1"], \
            group_anno_1_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_1_line_colour), \
            linewidth = group_anno_1_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_1_1]. \
            annotate('', xy = (group_anno_1_line_x_offset_end - \
            group_corr_dict["G1"], \
            group_anno_1_line_y_offset_end), \
            xycoords = 'data', \
            xytext = (group_anno_1_line_x_tag_end, \
            group_anno_1_line_y_tag_end + \
            (group_anno_1_line_y_offset_end - \
            group_anno_1_line_y_offset_start)), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_1_line_colour), \
            linewidth = group_anno_1_line_width), \
            annotation_clip = False)
            
    if group_anno_2 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_2_2 = group_anno_2_start
        
        group_dict[taxon_2_2].annotate \
            ('', xy = (group_anno_2_line_x_offset_start, \
            group_anno_2_line_y_offset_start + \
            group_corr_line_dict["G2"]), \
            xycoords = 'data', xytext = (group_anno_2_line_x_offset_end, \
            group_anno_2_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_2_line_colour), \
            linewidth = group_anno_2_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_2_2].annotate \
            (group_anno_2_title, textcoords = "data", \
             xy = (group_anno_2_line_x_offset_start - 5, \
            (group_anno_2_line_y_offset_start + \
            (group_anno_2_line_y_offset_end - \
            group_anno_2_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, ha = "center", \
            va = "top", weight = bold_on_off(group_anno_2_title_bold), \
            fontsize =group_anno_2_title_font_size, \
            color = colour(group_anno_2_title_colour ))
            
        group_dict[taxon_2_2].\
            annotate('', xy = (group_anno_2_line_x_tag_end, \
            group_anno_2_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_2_line_x_offset_start - factor, \
            group_anno_2_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_2_line_colour), \
            linewidth = group_anno_2_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_2_2]. \
            annotate('', xy = (group_anno_2_line_x_offset_end - \
            factor_2, group_anno_2_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_2_line_x_tag_end, \
            group_anno_2_line_y_tag_end + \
            (group_anno_2_line_y_offset_end - \
            group_anno_2_line_y_offset_start)), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_2_line_colour), \
            linewidth = group_anno_2_line_width), \
            annotation_clip = False)   
            
    if group_anno_3 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_3_3 = group_anno_3_start
        
        group_dict[taxon_3_3].\
            annotate('', xy = (group_anno_3_line_x_offset_start, \
                     group_anno_3_line_y_offset_start + \
                     group_corr_line_dict["G3"]), \
                     xycoords = 'data', \
                     xytext = (group_anno_3_line_x_offset_end, \
                     group_anno_3_line_y_offset_end ), \
                     arrowprops = dict(arrowstyle = "-", \
                     color = colour(group_anno_3_line_colour), \
                     linewidth = group_anno_3_line_width), \
                     annotation_clip = False)
                
        group_dict[taxon_3_3]. \
            annotate(group_anno_3_title, textcoords = "data", \
            xy= (group_anno_3_line_x_offset_start - 5, \
            (group_anno_3_line_y_offset_start + \
            (group_anno_3_line_y_offset_end - \
            group_anno_3_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, \
            ha = "center", va = "top", \
            weight = bold_on_off(group_anno_3_title_bold), \
            fontsize = group_anno_3_title_font_size, \
            color = colour(group_anno_3_title_colour ))
            
        group_dict[taxon_3_3]. \
            annotate('', xy = (group_anno_3_line_x_tag_end, \
            group_anno_3_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_3_line_x_offset_start - \
            factor, group_anno_3_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_3_line_colour), \
            linewidth = group_anno_3_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_3_3]. \
            annotate('', xy = (group_anno_3_line_x_offset_end - factor_2, \
            group_anno_3_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_3_line_x_tag_end, \
            group_anno_3_line_y_tag_end + \
            (group_anno_3_line_y_offset_end - \
            group_anno_3_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_3_line_colour), \
            linewidth = group_anno_3_line_width), \
            annotation_clip = False)  
    
    if group_anno_4 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_4_4 = group_anno_4_start
        
        group_dict[taxon_4_4]. \
            annotate('', xy = (group_anno_4_line_x_offset_start, \
            group_anno_4_line_y_offset_start + \
            group_corr_line_dict["G4"]), \
            xycoords = 'data', \
            xytext = (group_anno_4_line_x_offset_end, \
            group_anno_4_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_4_line_colour), \
            linewidth = group_anno_4_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_4_4]. \
            annotate(group_anno_4_title, textcoords = "data", \
            xy= (group_anno_4_line_x_offset_start - 5, \
            (group_anno_4_line_y_offset_start + \
            (group_anno_4_line_y_offset_end - \
             group_anno_4_line_y_offset_start) / 2)), \
             annotation_clip = False, rotation = 90, \
             ha = "center", va = "top", \
             weight = bold_on_off(group_anno_4_title_bold), \
             fontsize = group_anno_4_title_font_size, \
             color = colour(group_anno_4_title_colour ))
            
        group_dict[taxon_4_4]. \
            annotate('', xy = (group_anno_4_line_x_tag_end, \
            group_anno_4_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_4_line_x_offset_start - \
            factor, group_anno_4_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_4_line_colour), \
            linewidth = group_anno_4_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_4_4]. \
            annotate('', xy = (group_anno_4_line_x_offset_end - factor_2, \
            group_anno_4_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_4_line_x_tag_end, \
            group_anno_4_line_y_tag_end + \
            (group_anno_4_line_y_offset_end - \
            group_anno_4_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_4_line_colour), \
            linewidth = group_anno_4_line_width), \
            annotation_clip = False)
                
    if group_anno_5 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_5_5 = group_anno_5_start
        
        group_dict[taxon_5_5]. \
            annotate('', xy = (group_anno_5_line_x_offset_start, \
            group_anno_5_line_y_offset_start + \
            group_corr_line_dict["G5"]), \
            xycoords = 'data', \
            xytext = (group_anno_5_line_x_offset_end, \
            group_anno_5_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_5_line_colour), \
            linewidth = group_anno_5_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_5_5]. \
            annotate(group_anno_5_title, textcoords = "data", \
            xy= (group_anno_5_line_x_offset_start - 5, \
            (group_anno_5_line_y_offset_start + \
            (group_anno_5_line_y_offset_end - \
            group_anno_5_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, \
            ha = "center", va = "top", \
            weight = bold_on_off(group_anno_5_title_bold), \
            fontsize = group_anno_5_title_font_size, \
            color = colour(group_anno_5_title_colour))
            
        group_dict[taxon_5_5]. \
            annotate('', xy = (group_anno_5_line_x_tag_end, \
            group_anno_5_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_5_line_x_offset_start - \
            factor, group_anno_5_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_5_line_colour), \
            linewidth = group_anno_5_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_5_5]. \
            annotate('', xy = (group_anno_5_line_x_offset_end - factor_2, \
            group_anno_5_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_5_line_x_tag_end, \
            group_anno_5_line_y_tag_end + \
            (group_anno_5_line_y_offset_end - \
            group_anno_5_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_5_line_colour), \
            linewidth = group_anno_5_line_width), \
            annotation_clip = False)  
            
    if group_anno_6 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_6_6 = group_anno_6_start
        
        group_dict[taxon_6_6]. \
            annotate('', xy = (group_anno_6_line_x_offset_start, \
                     group_anno_6_line_y_offset_start + \
                     group_corr_line_dict["G6"]), \
                     xycoords = 'data', \
                     xytext = (group_anno_6_line_x_offset_end, \
                     group_anno_6_line_y_offset_end ), \
                     arrowprops = dict(arrowstyle = "-", \
                     color = colour(group_anno_6_line_colour), \
                     linewidth = group_anno_6_line_width), \
                     annotation_clip = False)
                
        group_dict[taxon_6_6]. \
            annotate(group_anno_6_title, textcoords = "data", \
            xy= (group_anno_6_line_x_offset_start - 5, \
            (group_anno_6_line_y_offset_start + \
            (group_anno_6_line_y_offset_end - \
             group_anno_6_line_y_offset_start) / 2)), \
             annotation_clip = False, rotation = 90, \
             ha = "center", va = "top", \
             weight = bold_on_off(group_anno_6_title_bold), \
             fontsize = group_anno_6_title_font_size, \
             color = colour(group_anno_6_title_colour ))
            
        group_dict[taxon_6_6]. \
            annotate('', xy = (group_anno_6_line_x_tag_end, \
            group_anno_6_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_6_line_x_offset_start - \
            factor, group_anno_6_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_6_line_colour), \
            linewidth = group_anno_6_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_6_6]. \
            annotate('', xy = (group_anno_6_line_x_offset_end - factor_2, \
            group_anno_6_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_6_line_x_tag_end, \
            group_anno_6_line_y_tag_end + \
            (group_anno_6_line_y_offset_end - \
            group_anno_6_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_6_line_colour), \
            linewidth = group_anno_6_line_width), \
            annotation_clip = False)  
            
    if group_anno_7 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
        
        taxon_7_7 = group_anno_7_start
        
        group_dict[taxon_7_7]. \
            annotate('', xy = (group_anno_7_line_x_offset_start, \
            group_anno_7_line_y_offset_start + \
            group_corr_line_dict["G7"]), \
            xycoords = 'data', \
            xytext = (group_anno_7_line_x_offset_end, \
            group_anno_7_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_7_line_colour), \
            linewidth = group_anno_7_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_7_7]. \
            annotate(group_anno_7_title, textcoords = "data", \
            xy= (group_anno_7_line_x_offset_start - 5, \
            (group_anno_7_line_y_offset_start + \
            (group_anno_7_line_y_offset_end - \
            group_anno_7_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, \
            ha = "center", va = "top", \
            weight = bold_on_off(group_anno_7_title_bold), \
            fontsize = group_anno_7_title_font_size, \
            color = colour(group_anno_7_title_colour ))
            
        group_dict[taxon_7_7]. \
            annotate('', xy = (group_anno_7_line_x_tag_end, \
            group_anno_7_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_7_line_x_offset_start - \
            factor, group_anno_7_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_7_line_colour), \
            linewidth = group_anno_7_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_7_7]. \
            annotate('', xy = (group_anno_7_line_x_offset_end - factor_2, \
            group_anno_7_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_7_line_x_tag_end, \
            group_anno_7_line_y_tag_end + \
            (group_anno_7_line_y_offset_end - \
            group_anno_7_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_7_line_colour), \
            linewidth = group_anno_7_line_width), \
            annotation_clip = False)  
                
    if group_anno_8 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_8_8 = group_anno_8_start
        
        group_dict[taxon_8_8]. \
            annotate('', xy = (group_anno_8_line_x_offset_start, \
            group_anno_8_line_y_offset_start + \
            group_corr_line_dict["G8"]), \
            xycoords = 'data', \
            xytext = (group_anno_8_line_x_offset_end, \
            group_anno_8_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_8_line_colour), \
            linewidth = group_anno_8_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_8_8]. \
            annotate(group_anno_8_title, textcoords = "data", \
            xy= (group_anno_8_line_x_offset_start - 5, \
            (group_anno_8_line_y_offset_start + \
            (group_anno_8_line_y_offset_end - \
            group_anno_8_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, \
            ha = "center", va = "top", \
            weight = bold_on_off(group_anno_8_title_bold), \
            fontsize = group_anno_8_title_font_size, \
            color = colour(group_anno_8_title_colour ))
            
        group_dict[taxon_8_8]. \
            annotate('', xy = (group_anno_8_line_x_tag_end, \
            group_anno_8_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_8_line_x_offset_start - \
            factor, group_anno_8_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_8_line_colour), \
            linewidth = group_anno_8_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_8_8]. \
            annotate('', xy = (group_anno_8_line_x_offset_end - factor_2, \
            group_anno_8_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_8_line_x_tag_end, \
            group_anno_8_line_y_tag_end + \
            (group_anno_8_line_y_offset_end - \
            group_anno_8_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_8_line_colour), \
            linewidth = group_anno_8_line_width), \
            annotation_clip = False)  
                
    if group_anno_9 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_9_9 = group_anno_9_start
        
        group_dict[taxon_9_9]. \
            annotate('', xy = (group_anno_9_line_x_offset_start, \
            group_anno_9_line_y_offset_start + \
            group_corr_line_dict["G9"]), \
            xycoords = 'data', \
            xytext = (group_anno_9_line_x_offset_end, \
            group_anno_9_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_9_line_colour), \
            linewidth = group_anno_9_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_9_9]. \
            annotate(group_anno_9_title, textcoords = "data", \
            xy= (group_anno_9_line_x_offset_start - 5, \
            (group_anno_9_line_y_offset_start + \
            (group_anno_9_line_y_offset_end - \
            group_anno_9_line_y_offset_start) / 2)), \
            annotation_clip = False, rotation = 90, \
            ha = "center", va = "top", \
            weight = bold_on_off(group_anno_9_title_bold), \
            fontsize = group_anno_9_title_font_size, \
            color = colour(group_anno_9_title_colour))
            
        group_dict[taxon_9_9]. \
            annotate('', xy = (group_anno_9_line_x_tag_end, \
            group_anno_9_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_9_line_x_offset_start - \
            factor, group_anno_9_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_9_line_colour), \
            linewidth = group_anno_9_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_9_9]. \
            annotate('', xy = (group_anno_9_line_x_offset_end - factor_2, \
            group_anno_9_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_9_line_x_tag_end, \
            group_anno_9_line_y_tag_end + \
            (group_anno_9_line_y_offset_end - \
            group_anno_9_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_9_line_colour), \
            linewidth = group_anno_9_line_width), \
            annotation_clip = False) 
                
    if group_anno_10 == "on":
        group_dict = {taxons: graphs for taxons, graphs \
                      in zip(data_list, ax_list)}
            
        taxon_10_10 = group_anno_10_start
        
        group_dict[taxon_10_10]. \
            annotate('', xy = (group_anno_10_line_x_offset_start, \
            group_anno_10_line_y_offset_start + \
            group_corr_line_dict["G10"]), \
            xycoords = 'data', \
            xytext = (group_anno_10_line_x_offset_end, \
            group_anno_10_line_y_offset_end ), \
            arrowprops = dict(arrowstyle = "-", \
            color = colour(group_anno_10_line_colour), \
            linewidth = group_anno_10_line_width), \
            annotation_clip = False)
                
        group_dict[taxon_10_10]. \
            annotate(group_anno_10_title, textcoords = "data", \
            xy= (group_anno_10_line_x_offset_start - 5, \
            (group_anno_10_line_y_offset_start + \
            (group_anno_10_line_y_offset_end - \
             group_anno_10_line_y_offset_start) / 2)), \
             annotation_clip = False, rotation = 90, \
             ha = "center", va = "top", \
             weight = bold_on_off(group_anno_10_title_bold), \
             fontsize = group_anno_10_title_font_size, \
             color = colour(group_anno_10_title_colour ))
            
        group_dict[taxon_10_10]. \
            annotate('', xy = (group_anno_10_line_x_tag_end, \
            group_anno_10_line_y_tag_end), xycoords = 'data', \
            xytext = (group_anno_10_line_x_offset_start - \
            factor, group_anno_10_line_y_offset_start), \
            arrowprops = dict(arrowstyle = "-", color = \
            colour(group_anno_10_line_colour), \
            linewidth = group_anno_10_line_width), \
            annotation_clip = False)
            
        group_dict[taxon_10_10]. \
            annotate('', xy = (group_anno_10_line_x_offset_end - factor_2, \
            group_anno_10_line_y_offset_end), xycoords = 'data', \
            xytext = (group_anno_10_line_x_tag_end, \
            group_anno_10_line_y_tag_end + \
            (group_anno_10_line_y_offset_end - \
            group_anno_10_line_y_offset_start)), \
            arrowprops = dict(arrowstyle ="-", \
            color = colour(group_anno_10_line_colour), \
            linewidth = group_anno_10_line_width), \
            annotation_clip = False)  
    
    ###########################################################################
    ###########################################################################
    # Saves the overall plot to your selected folder stated in the Parameter
    # file. Choose png, svg or pdf in the parameter file. Can choose to save
    # as alltypes in one go if sate all seperate by comma such as svg,png,pdf.
    print("")
    print("\n **Saving {}**".format(par_dict["Save as**"]))
    
    # Obtain saving formate from Parameter file
    save_list = par_dict["Save as**"].replace(" ","").lower()
    save_list = list(save_list.split(","))
    
    # Error check entries and save
    if "pdf" not in save_list and "png" not in save_list and "svg" not in \
        save_list:
        print("\nImage format type is not recognised. Is not png, svg or pdf."
              " Check your parameter file entry.")
        sys.exit()
        
    if "pdf" in save_list:
        plt.savefig(f"{output_name}.pdf")
        print("")
        print("\n**The pdf has been saved**")
        
    if "png" in save_list:
        try:
            dpi_num = float(str(par_dict["Png dpi"]).replace(" ",""))
        except:
            print("\nProblem with dpi entry in Parameter file. Check it is "
                  "numeric and a sensible value. Values between 75 for a"
                  " coarse resolution and 1000 for a high resolution image"
                  " are most likely.")
            sys.exit()
                        
        if pd.isnull(dpi_num) == True:
            print("\nDpi entry required in Parameter file if png is"
                  " specified as output format.")
            sys.exit()
            
        plt.savefig(f"{output_name}.png", dpi = dpi_num)
        print("")
        print("\n**The png has been saved**")
        
    if "svg" in save_list:
        plt.savefig(f"{output_name}.svg")
        print("")
        print("\n**The svg has been saved.**")
    
    # Print closing message about author, year of program production and
    # authors location.
    print("")
    print("# P4 (Python Palaeo Plotting Program) #")
    print("# Written by Dr Antony Blundell #")
    print("# School of Geography #")
    print("# University of Leeds, 2022 #")
    print("")
    
###############################################################################
###############################################################################
if __name__ == "__main__":
    main()    

###############################################################################
###############################################################################