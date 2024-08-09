#!/usr/bin/env python

import argparse
import bioinfo  
#import numpy as np
import gzip
#import itertools as it


#"valid_BC_path = /projects/bgmp/shared/2017_sequencing/indexes.txt"

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-r1", "--r1", help="To specify the R1 input fastq file", type=str,required=True)
    parser.add_argument("-r2", "--r2", help="To specify the R2 input fastq file", type=str,required=True)
    parser.add_argument("-r3", "--r3", help="To specify the R3 input fastq file", type=str,required=True)
    parser.add_argument("-r4", "--r4", help="To specify the R4 input fastq file", type=str,required=True)
    parser.add_argument("-qs_cutoff", "--qs_cutoff", help="To specify minumum average quality score", type=int,required=True)
    parser.add_argument("-seq_BC", "--seq_BC", help="To specify txt file containing all valid barcodes", type=str,required=True)
    return parser.parse_args()
	
args = get_args()

#assign global variables
r1 = args.r1
r2 = args.r2
r3 = args.r3
r4 = args.r4
qs_cutoff = args.qs_cutoff
seq_BC = args.seq_BC

# valid barcodes
# B1	GTAGCGTA    A5	CGATCGAT    C1	GATCAAGG
# B9	AACAGCGA    C9	TAGCCATG    C3	CGGTAATC
# B3	CTCTGGAT    C4	TACCGGAT    A11	CTAGCTCA
# C7	CACTTCAC    B2	GCTACTCT    A1	ACGATCAG
# B7	TATGGCAC    A3	TGTTCCGT    B4	GTCCTAAG
# A12	TCGACAAG    C10	TCTTCGAC    A2	ATCATGCG
# C2	ATCGTGGT    A10	TCGAGAGT    B8	TCGGATTC
# A7	GATCTTGC    B10	AGAGTCCA    A8	AGGATAGC

#open zipped fastq files to read
r1_fh = gzip.open(r1,'rt')
r2_fh = gzip.open(r2,'rt')
r3_fh = gzip.open(r3,'rt')
r4_fh = gzip.open(r4,'rt')

#establish valid BCs set
valid_BC = set()
first_line = True
with open(seq_BC,'r') as fh:     #next time can use fh.readline() before for-loop
    for line in fh:
        line = line.strip().split('\t')
        if first_line == True:
            first_line = False
            continue
        valid_BC.add(line[4])


#dictionaries 
#key is index, value is number of times observed
R1_writing_dict = {}
R2_writing_dict = {}

#open new fastq files to write - unknown index

R1_writing_dict["unknown_R1"]=open("output_fastq/unknown_R1.fastq", "w")
R2_writing_dict["unknown_R2"]=open("output_fastq/unknown_R2.fastq", "w")

#open new fastq files to write - hopped index
R1_writing_dict["hopped_R1"]=open("output_fastq/hopped_R1.fastq", "w")
R2_writing_dict["hopped_R2"]=open("output_fastq/hopped_R2.fastq", "w")


#open new fastq files to write - matched index
for index in valid_BC: 
    R1_writing_dict[index] = open(f"output_fastq/{index}_R1.fastq", "w")
    R2_writing_dict[index] = open(f"output_fastq/{index}_R2.fastq", "w")


# function to generate the reverse compliment
complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}  #dictionary of complement bases

def rev_comp(seq:str)->str:
    '''A function that takes a DNA sequence(string) and generate a reverse complement (string). Remember to import bioinfo.py'''
    seq = seq.strip()
    rev_comp=""
    rev_seq = seq[::-1]
    valid_seq = bioinfo.validate_base_seq(seq)
    if valid_seq == True:
        rev_comp_list = [complement[base] for base in rev_seq]
        # for base in rev_comp_list:
        #     rev_comp += base 
        rev_comp="".join(rev_comp_list)
    return rev_comp


def new_header(header:str, index_1:str, index_2:str )-> str:
    '''A function to append index information to the header'''
    #header += f" {index_1}-{index_2}\n"
    return f"{header} {index_1}-{index_2}\n"


# def mean_qual_score(qscore:str):
#     '''A function reads the qscore line (str) and generates a mean quality score value (int). Remember to import bioinfo.py'''
#     mean_qual_score = np.mean(bioinfo.convert_phred(qscore))
#     return mean_qual_score

#created counters
hopped_dict = {}
matched_dict = {}
total_unknown = 0

i = 0
header_info = {}
for line_r1, line_r2, line_r3, line_r4 in zip(r1_fh, r2_fh, r3_fh, r4_fh):
    #header list
    if i %4 == 0:
        header_info = {'R1':line_r1.strip(),'R4':line_r4.strip()}

    if i % 4 == 1: # sequence
        index1 = line_r2.strip()
        index2 = rev_comp(line_r3.strip())
        R1_seq = line_r1
        R2_seq = line_r4
    if i % 4 == 3: #qual score 
        i1_qscore = line_r2.strip()
        i2_qscore = line_r3.strip()
        R1_qscore = line_r1
        R2_qscore = line_r4

        R1_fq = f"{new_header(header_info['R1'], index1, index2)}{R1_seq}+\n{R1_qscore}"
        #header_info["r1"] was empty when printed
        R2_fq = f"{new_header(header_info['R4'], index1, index2)}{R2_seq}+\n{R2_qscore}"

        if index1 not in valid_BC or index2 not in valid_BC or bioinfo.qual_score(i1_qscore) < qs_cutoff or bioinfo.qual_score(i2_qscore) < qs_cutoff:
            R1_writing_dict['unknown_R1'].write(R1_fq)
            R2_writing_dict['unknown_R2'].write(R2_fq)
            #write new header, seq line, + and q-score to UNKNOWN
            total_unknown += 1
            #increment counter

        elif index1 == index2:
            R1_writing_dict[index1].write(R1_fq)
            R2_writing_dict[index2].write(R2_fq)
                #write new header, seq line, + and q-score to MATCHED
            matched_key = f'{index1}-{index2}'
            if matched_key in matched_dict:
                matched_dict[matched_key] += 1
            else:
                matched_dict[matched_key] = 1

        elif index1 != index2:
            R1_writing_dict["hopped_R1"].write(R1_fq)
            R2_writing_dict["hopped_R2"].write(R2_fq)
            #write new header, seq line, + and q-score to HOPPED
            hopped_key = f'{index1}-{index2}'
            if hopped_key in hopped_dict:
                hopped_dict[hopped_key] += 1
            else:
                hopped_dict[hopped_key] = 1
        
        else:
            print("logic failed")
    i += 1
    

#close all files

for fh in R1_writing_dict.values():
    fh.close()
for fh in R2_writing_dict.values():
    fh.close()

#Stats

total_matched = sum(matched_dict.values())
total_hopped = sum(hopped_dict.values())

total_records = total_unknown + total_hopped + total_matched

with open('demux_summary.txt', 'w') as out_file:
    out_file.write(f'Read Summary - QScore Cutoff: {qs_cutoff} \n')
    out_file.write('\n')

    out_file.write(f'R1 Input Fastq: {r1}\n')
    out_file.write(f'R2 Input Fastq: {r2}\n')
    out_file.write(f'R3 Input Fastq: {r3}\n')
    out_file.write(f'R4 Input Fastq: {r4}\n')

    out_file.write('\n')
    out_file.write(f'Total Number of Reads:\n {total_records}\n')
    out_file.write('\n')
    out_file.write(f'Matched Reads: {(total_matched/total_records)*100}% ({total_matched} reads)\n')
    out_file.write(f'Hopped Reads: {(total_hopped/total_records)*100}% ({total_hopped} reads)\n')
    out_file.write(f'Unknown Reads: {(total_unknown/total_records)*100}% ({total_unknown} reads)\n')
    out_file.write('\n')
    out_file.write(f'Matched Reads per index \n')
    for matched_key in matched_dict:
        out_file.write(f'{matched_key}: {(matched_dict[matched_key]/total_records)*100}% ({matched_dict[matched_key]} reads)\n')




