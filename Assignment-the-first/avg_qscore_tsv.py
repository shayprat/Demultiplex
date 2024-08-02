#!/usr/bin/env python

import argparse
import bioinfo   
import numpy as np
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="Generate a per base distribution of mean quality scores for zipped FastQ files")
    parser.add_argument("-ifq", "--input_fastq", help="To specify the input fastq file", type=str,required=True)
    parser.add_argument("-seq_len", "--seq_len", help="To specify the length of the sequence line", type=int,required=True)
    return parser.parse_args()
	
args = get_args()

#assign global variables
input_fq=args.input_fastq
seq_len=args.seq_len


q_score_array = np.zeros(seq_len,dtype=float)

with gzip.open(input_fq,"rt") as file:
    record = 0 
    for i,line in enumerate(file):
        line = line.strip()
        if i % 4 == 3:                  
            for index,score in enumerate(line):
                q_score = bioinfo.convert_phred(score)
                q_score_array[index] += q_score
            record += 1


print(f"Pos\tMean Qual Score")

for i,sum in enumerate(q_score_array):
    mean_i = sum/record
    q_score_array[i] = mean_i
    
    print(f"{i}\t{mean_i}")



