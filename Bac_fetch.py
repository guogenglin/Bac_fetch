# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 10:35:20 2025

@author: Genglin Guo
@e-mail: 2019207025.njau.edu.cn
"""

import subprocess
import zipfile
import json
import pathlib
import re
import shutil

# the species name of the bacteria you want to download
species = 'Klebsiella michiganensis'
# define the output file name
outfilename = species[0] + '_' + species.split(' ')[1] + '.zip'
# the path of the output file
outfilepath = 'F:/' + outfilename

# the command you want, there are a lot of parameters you can modify
command = ['datasets', 'download', 'genome', 'taxon', species, '--assembly-source', 'RefSeq', 
           '--assembly-version', 'latest', '--exclude-atypical', '--filename', outfilepath, '--mag', 
           'exclude', '--annotated', '--fast-zip-validation', '--include', 'genome,seq-report']
# --assembly-level string 'chromosome,complete,contig,scaffold'
# run the command
process = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
# unzip the file
zipfile.ZipFile(outfilepath, 'r').extractall(outfilepath[:-4])

# parse the jsonl data summary jsonl file
data_list = []
jsonl_file = outfilepath[:-4] + '/ncbi_dataset/data/assembly_data_report.jsonl'
with open(jsonl_file, 'r', encoding='utf-8') as file:
    for line in file:
        data_list.append(json.loads(line.strip()))
# a info dict, you can personalize design a dict contain any infomation you can obtain from Biosample or Assembly
info_summary = dict()
for genome in data_list:
    info = genome['assemblyInfo']['biosample']['attributes']
    name, strain, date, host, country, isolate, sample, ident = '', '', '', '', '', '', '', ''
    for i in info:
        if i['name'] == 'strain':
            strain = i['value']
        elif i['name'] == 'collection_date':
            date = i['value'] if 'value' in i else 'NA'
        elif i['name'] == 'host':
            host = i['value']
        elif i['name'] == 'geo_loc_name':
            country = i['value']
        elif i['name'] == 'isolate':
            isolate = i['value']
        elif i['name'] == 'sample_name':
            sample = i['value']
    ident = genome['assemblyInfo']['assemblyName']
    # it's very hard to obtain the name because not everyone uploaded their genome as the same style
    if strain != '':
        name = strain
    elif isolate != '':
        name = isolate
    elif sample != '':
        name = sample
    elif ident != '':
        name = ident
    else:
        # in case some name is missing
        print('no name for {}'.format(genome['accession']))
    # remove the space within the name, space will cause problems during analysis, so as '(' and ')'
    if ' ' in name or '(' in name or ')' in name or ':' in name or '/' in name or '\\' in name:
        trans_table = str.maketrans(' ():/\\', '______')  # 将 'a' 和 'c' 映射为 'b'
        name = name.translate(trans_table)
    # the format of date is xxxx-xx-xx, for example, 2025-09-09, a regular expression was used to identify them
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date):
        date = 'NA'
    else:
        # year is the most common used date infomation, if you want more, you can modify the code in the next line
        date = date.strip().split('-')[0]
    # see? everyone have a different way to say NA
    if host.lower() in ['not determined', 'missing', 'none', 'not applicable', 'n/a', '', 'not collected', 'na']:
        host = 'NA'
    # The rest part I'm trying to consice the diversity species name, there are many way to present 'human', ' pig', but only one should be recorded for futher analysis
    elif any(keyword in host.lower() for keyword in ['homo sapiens', 'male', 'female', 'patient', 'human']):
        host = 'Human'
    elif any(keyword in host.lower() for keyword in ['bactrocera dorsalis', 'ceratitis capitata', 'drosophila', 'anastrepha fraterculus', 'stomoxys', 'musca domestica']):
        host = 'Fruit fly'
    elif any(keyword in host.lower() for keyword in ['zea mays', 'ustilago maydis']):
        host = 'Corn'
    elif any(keyword in host.lower() for keyword in ['gallus gallus']):
        host = 'Chicken'
    elif any(keyword in host.lower() for keyword in ['serpentes']):
        host = 'Snake'
    elif any(keyword in host.lower() for keyword in ['cow', 'cattle', 'bos taurus']):
        host = 'Cattle'
    elif any(keyword in host.lower() for keyword in ['capra hircus']):
        host = 'Goat'
    elif any(keyword in host.lower() for keyword in ['sus scrofa', 'pig']):
        host = 'Pig'
    else:
        host = host.capitalize()
    # like the date, country/region is also contain more infomation, for example, China: Nanjing, normally we only need country/region
    # You should be careful to use the word, a single word "country" is not precise.
    if ': ' not in country:
        country = 'NA'
    else:
        country = country.strip().split(':')[0]
    info_summary[genome['accession']] = {'Name' : name, 
                               'Date' : date, 
                               'Host' : host, 
                               'Country/Region' : country}
# These code was used to screen how many hosts we have screened, and we can recognize if there are duplicate, and modify the code above
'''
hosts = []
for accession in info_summary.values():
    if accession['Host'] not in hosts:
        hosts.append(accession['Host'])
'''

# make a dir to save the genome file, the file name will be replaced by the name of bacteria
genome_outdir = outfilepath[:-4] + '/genome/'
if not pathlib.Path(genome_outdir).exists():
    pathlib.Path(genome_outdir).mkdir()
# generate a summary table to store the information we need
out_summary_table = open(str(genome_outdir + '/data_summary.tsv'), 'wt')
out_summary_table.write('Name\tYear\tHost\tCountry/Region\tAccession\n')
# check if there are duplicate name
name_list = []
for accession, infomation in info_summary.items():
    out_summary_table.write(infomation['Name'])
    out_summary_table.write('\t')
    out_summary_table.write(infomation['Date'])
    out_summary_table.write('\t')
    out_summary_table.write(infomation['Host'])
    out_summary_table.write('\t')
    out_summary_table.write(infomation['Country/Region'])
    out_summary_table.write('\t')
    out_summary_table.write(accession)
    out_summary_table.write('\n')
    origin_path = outfilepath[:-4] + '/ncbi_dataset/data/' + accession
    if infomation['Name'] not in name_list:
        name_list.append(infomation['Name'])
    else:
        print('Accession:{}, Name: {}, there are already a genome sequence called this name, please check if they are the same.'.format(accession, infomation['Name']))
    new_path = genome_outdir + infomation['Name'] + '.fasta'
    for file in pathlib.Path(origin_path).iterdir():
        if str(file).endswith('.fna'):
            shutil.copy(file, new_path)

out_summary_table.close()

