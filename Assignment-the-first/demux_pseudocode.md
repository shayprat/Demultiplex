# Define the problem

1+ billion reads --> bucket them by sample barcode/index. Tricky thing to remember - indexes can have "N"s and therefore low quality or they can be hopped. 

# Game Plan:
    generate the reverse compliment of the sequence line in R3
        save as RC_R3 or something similar
    append seq_line in R2 and RC_R3 to header of R1.fq and R4.fq
        generates new fastq files: R1.R2.RC_R3.fq and R4.R2.RC_R3.fq (prob will change the name)
    
    check if sequence line of R2.fq and RC_R3 contain any "N's"
        if yes --> punt R1.R2.RC_R3.fq to "R1_unknown fastq" punt R4.R2.RC_R3.fq to "R2_unknown fastq"
    
    check if sequence line of R2.fq and RC_R3 is in the valid indices txt file
        if no --> punt R1.R2.RC_R3.fq to "R1_unknown fastq" punt R4.R2.RC_R3.fq to "R2_unknown fastq"

    check if sequence line of R2.fq == RC_R3 (do they match?)
        if no --> punt R1.R2.RC_R3.fq to "R1_unmatched fastq" punt R4.R2.RC_R3.fq to "R2_unmatched fastq"

        if yes --> punt R1.R2.RC_R3.fq to "R1_matched fastq" punt R4.R2.RC_R3.fq to "R2_matched fastq"

# PSEUDOCODE:

argparse! variables: r1 for R1.fq file, r2 for R2.fq file, r3 for R3.fq file, and r4 for R4.fq file, BC_list for list of valid indicies

change list of valid indicies text file to an actual list...valid_BC_list?

# function to generate the reverse compliment of R3
    def rev_comp(file):
        with open (file, "r") as fh:
        for i,sequence_line in enumerate(file):
                i % 4 == 3 (looking at sequecning line)
                    index = -1 #start at last base
                    generate the reverse compliment (save as variable "BC_2")
                        if index == "A":
                            index == "T"
                        if index == "C":
                            index == "G"
                        if index == "G";
                            index == "C"
                        if index == "T":
                            index == "A"
                        RC_R3 += index (append or concatinate reverse base to "R3_RC")
                    index += -1 (move over one base to the left)
            return BC_2?
                
    file = r3


# function to append index 1 and RC_index 2 to header to R1.fq and R4.fq    
    def new_fastq(file): #file is either R1.fq or R4.fq
        enumerate to sequence line of r2 and save as variable "BC_1"
        to header line of file (1 % 4 == 0?):
            append or concatinate "BC_1" and "BC_2" (tab separated?)
        save as few fastq file

# Unknown, Unmatched, Matched?
    with open R2:
        extract sequencing line (need to save again as BC_1?)
        if "N" in BC_1 or BC_1 not in "valid_BC_list"
            write new R1.fq (with BC_1 and BC_2 in header) to new text file (R1 Unknown.fastq)
            write new R4.fq (with BC_1 and BC_2 in header) to new text file (R2 Unknown.fastq)
        elif BC_1 != BC_2
            write new R1.fq (with BC_1 and BC_2 in header) to new text file (R1 unmatched.fastq)
            write new R4.fq (with BC_1 and BC_2 in header) to new text file (R2 unmatched.fastq)
        else:
            write new R1.fq (with BC_1 and BC_2 in header) to new text file (R1 matched.fastq)
            write new R4.fq (with BC_1 and BC_2 in header) to new text file (R2 matched.fastq)









    
        
        
        