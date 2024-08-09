#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --mem=100G
#SBATCH --job-name=demux


/usr/bin/time -v python demux_the_3rd.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -qs_cutoff 26 -seq_BC /projects/bgmp/shared/2017_sequencing/indexes.txt 


