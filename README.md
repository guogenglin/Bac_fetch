# Bac_fetch
A python script to batch download bacteria genome sequences from NCBI
You can batch download any bacteria genome from NCBI by using this script, you can personalize the filter just like in the "Genome" database NCBI website, this part is depend on the "datasets" tool provided by NCBI, so all the parameters could be modified according to the "datasets" manual.
After the genome sequences you want downloaded, it will also generate a infomation table of these bacteria isolates/strains, the default is "Host", "Collection date", and "Country/Region", you can also personalize it by modify the code. The table will be named as "data_summary.tsv" and saved in the dictionary where you saved your genome sequences.
Also, the file name of these downloaded genome sequence will be replaced by their name, instead of accession.

# External Dependencies
Datasets

# Usage
Acturally, there are no need to write a usage because this is a very simple script, but I still need to clarify how to use it, I haven't give a input example because the requirement of everyone is different and the parameters will be too much. Here, follow these steps, I will show you how to download the genome sequence data as the way you want.

1. Assign the variable 'species' by the species name of the bacteria you want to download genome sequences.
2. Change the frist part of the variable 'outfilepath' to the path where you want to save the genome data.
3. (Optional) If you want to modify the parameters to download genome sequence data, you may modify the list 'command' according to the manual of 'datasets'. For example, you may want to restrict the assembly level to complete, then you should add '--assembly-level string', 'complete' into the list.
4. (Optional) 'data_list' is a very big list contains a large amount of informations, you can extract more information you want, if you did, you should also change the output part.
5. The uploaders of these genome sequences have many way to describe the host, for example, you may see 'Sus scrofa', 'hog', 'swine', 'porcine', etc. these are all pigs, so I've written some code to unify them, however, my ability is limited, the code I provided is very complicate, and need real-time update (depend on if it could fulfilling my needs). You can also revise it to meet your needs.
