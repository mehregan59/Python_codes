The cod has two parts. In the first part it accepts the results of software like Virsorter2, VIBRANT and DeepVirfinder in txt. 
It is better to rename name of each file to corresponding software. You need to add all files in one folder. When you run the code,
it asks you about the desire minimum length of contig, the minimum score of virus identification, which software you want to select 
to save contigs in selected_contigs.csv. before answering this question, it shows you a list of names based on name of your files, 
because each file is supposed to be from one software and you can select one of them. Last question is about fna file which is a 
file that contain sequences. If you type “yes” the code will filter sequence based on your answered to other three questions. 
 
The output of first part includes two csv files (combine_data.csv and selected_contigs.csv).  first csv file (combine_data.csv) 
includes data from all software together without any selection, and the second file (selected_contigs.csv) is all contigs selected based on the parameter you selected. 
The second part of the cod only run if you have sequence file with fna extension in your folder. It filters your sequence file 
based the parameters you selected. Then it saves a file with same name of your fna file but it add word filter to it. 
You can try the code with provided example file.   
