#!/usr/bin/env python

# Author: spratap@uoregon.edu

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = "ACTGNactgn"
RNA_bases = "ACUGNacugn"

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter)-33

def qual_score(phred_score: str) -> float:
    """ Converting each character to a ASCII qual score and measuring the average score of the string """
    sum_qual_score=0  
    for i, score in enumerate (phred_score): 
        sum_qual_score+=convert_phred(score)
    
    return(sum_qual_score)/(i+1)

# def validate_base_seq(seq, RNAflag=False):
#     '''This function takes a string. Returns True if string is composed
#     of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
#     seq = seq.upper()
#     if DNA_bases or RNA_bases in seq:
#         return len(seq) == seq.count("A")+seq.count("U" if RNAflag else "T")+seq.count("G")+seq.count("C")+seq.count("N")

def validate_base_seq(seq: str, RNAflag: bool=False)-> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    seq = set(seq)
    if RNAflag:
        return set.issubset(seq,RNA_bases)
    else:
        return set.issubset(seq,DNA_bases)

def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(DNA, RNAflag=False)
    DNA=DNA.upper()
    gc_content = DNA.count("G")+DNA.count("C")
    return gc_content/len(DNA)

def calc_median(lst:list):
    '''Given a list, returns the median value of the list'''
    median=0
    lst.sort()
    length=len(lst)
    if length %2 == 0: #if even number of elements
        median=(lst[length//2] + lst[length//2-1])/2
        return median

    else:
        median = lst[length//2]
        return median

def oneline_fasta(input_fasta:str):
    '''collapese multiple sequence lines in a fasta into one line and generates new fasta file with one sequence line per record '''
    first_header=True
    output_fasta=input_fasta[:input_fasta.rfind(".")]+"_oneline.fasta"
    opened_output_fasta=open(output_fasta,"w")
    for line in input_fasta:
        line=line.strip()
        if line[0]==">":
            if first_header:
                header=line
                opened_output_fasta.write(header+"\n")
                first_header=False
            else:
                opened_output_fasta.write('\n')
                header=line
                opened_output_fasta.write(header+"\n")
        else:
            seq=line
            opened_output_fasta.write(seq)
    opened_output_fasta.close()
    return(output_fasta)
            
        

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert validate_base_seq("AATAGAT") == True, "DNA string not recognized"
    print("Correctly identified a DNA string")
    assert validate_base_seq("Hi there!") == False, "Non-DNA identified as DNA"
    print("Correctly determined non-DNA")
    assert validate_base_seq("AATAGAT", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("TATUC",False) == False
    assert validate_base_seq("UCUGCU", False) == False
    print("Passed DNA and RNA tests")

    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("correctly calculated GC content")

    assert calc_median([1,2,100]) == 2, "calc_median function does not work for odd length list"
    assert calc_median([1,2]) == 1.5, "calc_median function does not work for even length list"
    print("Median successfully calculated")