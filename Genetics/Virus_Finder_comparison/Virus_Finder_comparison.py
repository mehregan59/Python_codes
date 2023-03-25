#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Fri Sep  9 16:38:47 2022

@author: Mehregan Ebrahimi
"""
import sys
import pandas as pd
from pathlib import Path
import glob
import os
import os.path

pd.set_option('display.max_columns', None)


if len (sys.argv) < 2:
    print("Need input! add complete path of folder that include files.")
    print("All files must include same column heading for same data!") 
    sys.exit(1)

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        print("your input = ", val)
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            print("your input = ", val)
        except ValueError:
            print("Input must be number")

def check_software(input):
    # check name in name file
    name = input
    if name in file_names:

        print("your input = ", name)
    else:
        ValueError
        print("Input must be from list above")
        quit()
#folder and file name to save data 
folder = sys.argv[1]
#folder = (r'D:\Mina\Python\Table\Lo2\\')
filepath = Path(folder + "selected_contigs.csv")
filepath2 = Path(folder + "combine_data.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
file_present = glob.glob(folder + "combine_data.csv")


length_value = int(input("What is the minmum length you want to select? "))
check_user_input(length_value)   
    
score_value = input("What is the minmum score you want to select? ")
check_user_input(score_value)  

file_names = []
for file in os.listdir(folder):
    if not file.endswith(".fna"):
        basename = os.path.basename(file)
        name = os.path.splitext(basename)[0]
        file_names.append(name)
        
software_name = input("Select a software from list below to filter sequence file based on it? \n" + str(file_names) + " ")
check_software(software_name)

fna_yes = input("Is there fna file in folder? ")
fna_present = fna_yes.upper()

try: 
    if fna_present == "YES" or  fna_present == "NO":   
        df_dic = {}  # dictionary to hold data
        if not file_present:
            for i in glob.glob(folder + "*.*"):
                if not i.endswith(".fna"):
                    basename = os.path.basename(i)
                    name = os.path.splitext(basename)[0]
                    #print(name)
                   # read csv into a dataframe and add it to dict with file_name as it key
                    df_dic[name] = pd.read_csv(i, sep='\t')
                #print(df_dic)
                #Combine all dfs
                all_df1 = pd.concat([df.assign(software=k) for k,df in df_dic.items()], ignore_index=True)
                #reshape df to make new df
                reshape_df1 = (all_df1.set_index(["contig_id", "software"])
                         .stack()
                         .reset_index(name='value')
                         .rename(columns={'level_2':'rest'}))
                reshape_df2 = reshape_df1.set_index(['contig_id','rest','software'])
                reshape_df2 = reshape_df2.unstack('software')
                reshape_df2.columns = [c[1] for c in reshape_df2.columns]
                reshape_df2 = reshape_df2.reset_index()
                table_final = reshape_df2.pivot(index='contig_id', columns='rest')
                table_final.to_csv(filepath2) 
            print("combine_data was saved")     
                #make list of key
            dfs = list(df_dic.keys())
            #go through dic and select row in dfs that have desired condition
            new_dic = {}
            #print(dfs)
            for i in dfs:
                temp_df = df_dic.get(i)
                if "score" in temp_df:
                    eidted_df = temp_df[(temp_df['score'] >= float(score_value))] 
                    new_dic [i] = eidted_df
                else:
                    new_dic [i] = temp_df
            #print(new_dic) 
            #Combine all dfs
            all_df = pd.concat([df.assign(software=k) for k,df in new_dic.items()], ignore_index=True)
            #print(all_df)
            #making filter for next part
            final_df1 = all_df[(all_df['software'] == software_name) & (all_df['length'] >= length_value) 
                                 & (all_df['warnings'].isna())]
            final_df1 = final_df1.reset_index(drop=True)
            #print(final_df1)
            remain_df = pd.merge(all_df,final_df1, indicator=True, how='outer')\
                    .query('_merge=="left_only"')\
                        .drop('_merge', axis=1)
            #print(remain_df)
            all_duplicate = remain_df[remain_df.groupby('contig_id')['contig_id'].transform('size') > 2]
            #print(all_duplicate)
            final_df2 = all_duplicate[(all_duplicate['software'] == software_name)]
            final_df2 = final_df2.reset_index(drop=True)
            #print(final_df2)
            frames = [final_df1, final_df2]
            final_table = pd.concat(frames)
            final_table = final_table.dropna(axis='columns', how ='all')
            #print(final_table)
            final_table.to_csv(filepath) 
            print("selected_contigs was saved") 
            if fna_present == "YES":
                filter_column = final_table.loc[:,['contig_id']]
                #print(filter_column)
                vect = filter_column['contig_id'].tolist()
                #print(vect)
                AI_DICT = {}
                for line in vect:
                    #print(line)
                    AI_DICT[line] = 1  
                #print(AI_DICT)
                for file in glob.glob(folder + "*.*"):
                    if file.endswith(".fna"):
                        seq_file = file
                        #print(seq_file)
                #folder and file name to save data 
                basename = os.path.basename(seq_file)
                output1 ="Filtered_"+ basename
                filepath3 = Path(folder + output1)
                #print(filepath2)
                with open(seq_file, "rt") as fh:    
                    skip = 0
                    for line in fh:
                        if line[0] == '>':
                            _splitline = line.split('|')
                            accessorIDWithArrow = _splitline[0]
                            accessorID = accessorIDWithArrow[1:-1]
                            #print(accessorID)
                            if accessorID in AI_DICT:
                                with open(filepath3, "a") as fout:
                                    fout.write(line)
                                skip = 0
                            else:
                                skip = 1
                        else:
                            if not skip:
                                with open(filepath3, "a") as fout:
                                    fout.write(line)   
                print("Filtered sequence file was saved") 
        else:
            print('WARNING: This file already exists!')   
    else:
        print("Answer with yes or no only")
except Exception as error:   
    print("Heading columns of all files must be same!",
    error)