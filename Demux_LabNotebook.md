
7/24/2024 

ssh onto Talapas on VSCode
```$ pwd --> /home/spratap``` (need to get to base directory!)
Fast-Q files from 2017 in the following path:
```$ cd ../..
$ cd /projects/bgmp/shared/2017_sequencing/
$ ls -lah
```

    total 46G
    drwxrwsr-x+  3 coonrod  is.racs.pirg.bgmp 8.0K Apr 23 13:48 .
    drwxrwsr-x+ 42 sdwagner is.racs.pirg.bgmp 8.0K Jan 22  2024 ..
    -rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp  20G Jul 30  2018 1294_S1_L008_R1_001.fastq.gz
    -rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp 2.6G Jul 30  2018 1294_S1_L008_R2_001.fastq.gz
    -rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp 2.8G Jul 30  2018 1294_S1_L008_R3_001.fastq.gz
    -rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp  21G Jul 30  2018 1294_S1_L008_R4_001.fastq.gz
    drwxrws---+  2 coonrod  is.racs.pirg.bgmp 8.0K Jul  1  2022 demultiplexed
    -rwxrwxr-x+  1 sdwagner is.racs.pirg.bgmp  631 Aug  9  2021 indexes.txt
    -rw-r-xr--+  1 coonrod  is.racs.pirg.bgmp  327 Aug 16  2017 README.txt

**46G**...thems some fat files...

move onto a compute node 
    $ srun -A bgmp -p bgmp --mem=100gb -c 8 --pty bash

intial data exploration!
    $ zcat 1294_S1_L008_R1_001.fastq.gz | wc -l
        --> 1452986940 (this is how many lines, therefore 370M records)
    
    $ zcat 1294_S1_L008_R1_001.fastq.gz | head -4
        @K00337:83:HJKJNBBXX:8:1101:1265:1191 1:N:0:1
        GNCTGGCATTCCCAGAGACATCAGTACCCAGTTGGTTCAGACAGTTCCTCTATTGGTTGACAAGGTCTTCATTTCTAGTGATATCAACACGGTGTCTACAA
        +
        A#A-<FJJJ<JJJJJJJJJJJJJJJJJFJJJJFFJJFJJJAJJJJ-AJJJJJJJFFJJJJJJFFA-7<AJJJFFAJJJJJF<F--JJJJJJF-A-F7JJJJ
    
    $ zcat 1294_S1_L008_R2_001.fastq.gz | head -4
        @K00337:83:HJKJNBBXX:8:1101:1265:1191 2:N:0:1
        NCTTCGAC
        +
        #AA<FJJJ

    $ zcat 1294_S1_L008_R3_001.fastq.gz | head -4
        @K00337:83:HJKJNBBXX:8:1101:1265:1191 3:N:0:1
        NTCGAAGA
        +
        #AAAAJJF

    $ zcat 1294_S1_L008_R4_001.fastq.gz | head -4
        @K00337:83:HJKJNBBXX:8:1101:1265:1191 4:N:0:1
        NTTTTGATTTACCTTTCAGCCAATGAGAAGGCCGTTCATGCAGACTTTTTTAATGATTTTGAAGACCTTTTTGATGATGATGATGTCCAGTGAGGCCTCCC
        +
        #AAFAFJJ-----F---7-<FA-F<AFFA-JJJ77<FJFJFJJJJJJJJJJAFJFFAJJJJJJJJFJF7-AFFJJ7F7JFJJFJ7FFF--A<A7<-A-7--
R1 and R4 files are biological reads
R2 and R3 files are indexes


Determine the length of the reads in each file
(NOTE: Can't use zcat <filename> | head -4 | grep -A 1 ^@| grep -v ^@ | wc -c because counts newline! Need sed and awk... T__T)

```$ zcat 1294_S1_L008_R1_001.fastq.gz | head -4 | sed -n '2p'|awk '{print length($0)}'```
101

```$ zcat 1294_S1_L008_R2_001.fastq.gz | head -4 | sed -n '2p'|awk '{print length($0)}'```
8 

```$ zcat 1294_S1_L008_R3_001.fastq.gz | head -4 | sed -n '2p'|awk '{print length($0)}'```
8

```$ zcat 1294_S1_L008_R4_001.fastq.gz | head -4 | sed -n '2p'|awk '{print length($0)}'```
101

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | biological read | 101 | 33 |
| 1294_S1_L008_R2_001.fastq.gz | index | 9 | 33 |
| 1294_S1_L008_R3_001.fastq.gz | index | 9 | 33 |
| 1294_S1_L008_R4_001.fastq.gz | biological red |  101| 33 |

Phred33 because Qual Score line has symbols! (if only letters --> Phred64)

7/31/2024 ...what was I supposed to do for this assignment agian?


Created test files from large fastq file (these ARE NOT the ones needed for the input:output test.. these are just for data exploration and testing the py scripts on)

    i. headed the first 1 million records, piped the last 100 records to a test file in 

    ```$zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz |head -n 4000000 | tail -n 400 > R3_100record_test.fastq```

    repeat for all Rn files!

Run py script to generate .tsv with base position and average qualitiy score (```/home/spratap/bgmp/bioinfo/Bi622/Demultiplex/avg_qscore_tsv.py```)

SBATCH run for each read.fastq (```/home/spratap/bgmp/bioinfo/Bi622/Demultiplex/Avg_qscore.sh```)

Had the wrong shebang! Used ```#!usr/bin/bash python``` and got "cannot execute binary file" error --> changed to ```#!/bin/bash```

**Slurm Output**
R1 Job ID - 7820882
R2 Job ID - 7820883
R3 Job ID - 7820884
R4 Job ID - 7820885


Generated plots from tsv file using ```/home/spratap/bgmp/bioinfo/Bi622/Demultiplex/plt_qscore_distribution.py```
Shayal, figure out how to add images to markdown files...


What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer



How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)
Command for test files
```cat test_fastq_files/R2_100record_test.fastq | sed -n '2~4p'|grep  N | wc -l```

Command for actual files
```zcat 1294_S1_L008_R2_001.fastq.gz |sed -n '2~4p'|grep  N | wc -l```
Number of indeces with N's
R2 - 3976613
R3 - 3328051

**ACTUAL** test files for input:output 
input_test_R1.fastq
input_test_R2.fastq
input_test_R3.fastq
input_test_R4.fastq

Three (3) records per file to mimic 3 conditions - matched, hopped, and unknown

```zcat 1294_S1_L008_R1_001.fastq.gz | head -n 4```
1st record - likely to have N's (unknowns)
```zcat 1294_S1_L008_R1_001.fastq.gz | head -n 4000 | tail -n 4```
1000th record - either matched or unmatched? need to check same record number on R2 and R3
```zcat 1294_S1_L008_R1_001.fastq.gz | head -n 4000000 | tail -n 4```
1 millionth record - fingers crossed T__T

repeat for R2 - R4 files

1000th record still had N's in R2... maybe lets do the 5000th record and lets start with R2

NOTE: Number records to pull
-unknown - 3rd (```head -n 12```)
-hopped - why am I looking for it as if I'll actually find the actual record. manually generate an index without Ns that's not the rev_comp of each other T__T
-matched - 3 millionth (```head -n 12000000```)

LOL 3millionth record is the same index as the 2million record... should I buy a lotto ticket?