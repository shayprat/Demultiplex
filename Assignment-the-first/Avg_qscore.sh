#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --mem=16G
#SBATCH --job-name=R4_mean_qscore_per_base


#/usr/bin/time -v python avg_qscore_tsv.py -ifq /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -seq_len 101 > R1.tsv
#/usr/bin/time -v python avg_qscore_tsv.py -ifq /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -seq_len 8 > R2.tsv
#/usr/bin/time -v python avg_qscore_tsv.py -ifq /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -seq_len 8 > R3.tsv
/usr/bin/time -v python avg_qscore_tsv.py -ifq /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -seq_len 101 > R4.tsv

