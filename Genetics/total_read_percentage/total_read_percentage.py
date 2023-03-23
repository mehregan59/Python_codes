#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:41:33 2022

@author: mehregan59
"""

import glob
import sys
from pathlib import Path
import re
import pandas as pd

if len (sys.argv) < 2:
    print("Need input! add complete path of folder that include files.")
    sys.exit(1)

#folder and file name to save data 
folder = sys.argv[1]
filepath = Path(folder + "Read_percentage_table.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
files_present = glob.glob(folder + "Read_percentage_table.csv")
#actual program
if not files_present:
    for file in glob.glob(folder + "*.*"):
        fl=open(file)
        lines=fl.readlines()
        #print(file)
        name_str = ()
        with open(file, "rt") as f:
            firstline = f.readline().rstrip()
            find_name = re.search(r"in1=(\w*)(\_)", firstline , flags = re.I)
            name_str = find_name.group(1)
            symbols = [name_str]
            #making panda data frame
            data_table = pd.DataFrame(symbols)
            data_table.columns = ["ID"]
            data_table["Total_Read"] = 0
            data_table["Read_1"] = 0
            data_table["Percentage_read_1"] = 0
            data_table["Read_2"] = 0
            data_table["Percentage_read_2"] = 0 
            #loop to find data we need
            for  line in f:
                line = line.rstrip("\n")
                if line.startswith("Reads Used:"):
                    #find name of sample
                    read_used = re.search(r"Reads Used:(\s*)(\d*)(\s)", line)
                    #update data table with the name of sample
                    data_table.loc[data_table.ID == name_str, "Total_Read"] = float(read_used.group(2))
                if "Read 2 data:" in line:
                    for line in f:
                        if line.startswith("mapped:"):
                            #find second data
                            data_2_1= re.search(r"mapped:(\s*)(\d*\.\d*)", line)
                            data_2_2= re.search(r"mapped:(((\s*)(\d*\.\d*))(\S*)(\s*)(\d*))", line)
                            #update data table with second data 
                            data_table.loc[data_table.ID == name_str, "Read_2"] = float(data_2_2.group(7))
                            data_table.loc[data_table.ID == name_str, "Percentage_read_2"] = float(data_2_1.group(2))
        #prepare data frame for last entry
        with open(file, "rt") as f:
            for num, line in enumerate(f, 1):
                if "Read 1 data:" in line:
                    fromline = num
                if "Read 2 data:" in line:
                    toline = num
            store = lines[fromline:toline] 
            for line in store:
                    line = line.strip('\n\t')
                    if line.startswith("mapped:"):
                        #find last data
                        data_1_1 = re.search(r"mapped:(\s*)(\d*\.\d*)", line)
                        data_1_2= re.search(r"mapped:(((\s*)(\d*\.\d*))(\S*)(\s*)(\d*))", line)
                        #update data table with last data
                        data_table.loc[data_table.ID == name_str, "Read_1"] = float(data_1_2.group(7))
                        data_table.loc[data_table.ID == name_str, "Percentage_read_1"] = float(data_1_1.group(2))
                        #save data table to csv
                        data_table.to_csv(filepath, index = False, mode='a', header=not filepath.exists())
                        
else:
    print('WARNING: This file already exists!')
        