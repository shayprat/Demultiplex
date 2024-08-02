#!/usr/bin/env python

import matplotlib.pyplot as plt
import argparse
import re


def get_args():
    parser = argparse.ArgumentParser(description="Plot the mean quality scores distribution tsv files. Used with 'avg_qscore_tsv.py'")
    parser.add_argument("-tsv", "--input_tsv", help="To specify the input tsv file", type=str,required=True)
    return parser.parse_args()
	
args = get_args()

#assign global variables
input_tsv=args.input_tsv



base_pos = []
mean_qscore = []


first_line = True
for line in open(input_tsv,'r'):
    if first_line:
        first_line = False #skips the Pos \t Mean Qual Score line
        continue
    parts = line.strip().split()
    base_pos.append(int(parts[0]))
    mean_qscore.append(float(parts[1]))

read_name = input_tsv[0:input_tsv.rfind(".")]

plt.plot(base_pos,mean_qscore,color="red")
plt.xlabel("Base Position")
plt.ylabel("Mean Qual Score")
plt.title('Mean Q-Score Distribution per base - '+ str(read_name))
plt.savefig(read_name+"_mean_qscore_distribution.png")  
