## First, I will translate the user's sequence so that at the end, we can double-check the original and the RNAi-resistant protein sequences match.
def AATranslate(NucleotideSequence):

##This is a standard amino acid table (univeral "nuclear" translation table; not good for proteins translated in mitochondria)
    NucCodonDict={'ATT':'I',   'ATC':'I',  'ATA':'I',  'CTT':'L',  'CTC':'L',
    'CTA':'L',  'CTG':'L',  'TTA':'L',  'TTG':'L',  'GTT':'V',  'GTC':'V',
    'GTA':'V',  'GTG':'V',  'TTT':'F',  'TTC':'F',  'ATG':'M',  'TGT':'C',
    'TGC':'C',  'GCT':'A',  'GCC':'A',  'GCA':'A',  'GCG':'A',  'GGT':'G',
    'GGC':'G',  'GGA':'G',  'GGG':'G',  'CCT':'P',  'CCC':'P',  'CCA':'P',
    'CCG':'P',  'ACT':'T',  'ACC':'T',  'ACA':'T',  'ACG':'T',  'TCT':'S',
    'TCC':'S',  'TCA':'S',  'TCG':'S',  'AGT':'S',  'AGC':'S',  'TAT':'Y',
    'TAC':'Y',  'TGG':'W',  'CAA':'Q',  'CAG':'Q',  'AAT':'N',  'AAC':'N',
    'CAT':'H',  'CAC':'H',  'GAA':'E',  'GAG':'E',  'GAT':'D',  'GAC':'D',
    'AAA':'K',  'AAG':'K',  'CGT':'R',  'CGC':'R',  'CGA':'R',  'CGG':'R',
    'AGA':'R',  'AGG':'R',  'TAA':'*',  'TAG':'*',  'TGA':'*'}

    Protein =""
    for i in range (0,len(NucleotideSequence),3):
        codon = NucleotideSequence[i:i + 3]
        Protein += NucCodonDict[codon]
    return Protein

def AltCodon(UserSeq):

    ##This is my dictionary for the best alternative codon (using human codon frequency).
    ##Best alternative codon was determined in this manner, with the higher numbered items taking higher priority [there's a bit of subjectivity, though]:
    ##(1) The alternative codon codes for the same amino acid as the original codon (no alternative codons given for Met, Trp, or stop codons [-Term])
    ##(2) The most nucleotides was changed to generate the alternative codon (eg, for Leu, CTT was changed to TTG, not CTC)
    ##(3) The alternative codon was chosen to have the highest frequency of the remaining codons
    ##(4) Wobble base pairing was avoided. In particular, in the third position of the codon, A to G mutations and C to T mutations were avoided. A codon of lesser frequency was chosen in this case.

    HumanAltCodonDict={'AAA':'AAG','AAC':'AAT','AAG':'AAA','AAT':'AAC','ACA':'ACC','ACC':'ACA','ACG':'ACC','ACT':'ACC','AGA':'CGC','AGC':'TCC','AGG':'CGG','AGT':'TCC','ATA':'ATC','ATC':'ATA','ATG':'ATG','ATT':'ATC','CAA':'CAG','CAC':'CAT','CAG':'CAA','CAT':'CAC','CCA':'CCC','CCC':'CCA','CCG':'CCC','CCT':'CCC','CGA':'AGA','CGC':'AGA','CGG':'AGA','CGT':'CGG','CTA':'TTA','CTC':'CTG','CTG':'CTC','CTT':'TTG','GAA':'GAG','GAC':'GAT','GAG':'GAA','GAT':'GAC','GCA':'GCC','GCC':'GCT','GCG':'GCC','GCT':'GCA','GGA':'GGC','GGC':'GGA','GGG':'GGC','GGT':'GGC','GTA':'GTC','GTC':'GTG','GTG':'GTC','GTT':'GTG','TAA':'TAA','TAC':'TAT','TAG':'TAG','TAT':'TAC','TCA':'AGC','TCC':'AGC','TCG':'AGC','TCT':'AGC','TGA':'TGA','TGC':'TGT','TGG':'TGG','TGT':'TGC','TTA':'CTC','TTC':'TTT','TTG':'CTT','TTT':'TTC'}

    AltCodingSequence =""
    for i in range (0,len(UserSeq),3):
        codon = UserSeq[i:i + 3]
        AltCodingSequence += HumanAltCodonDict[codon]
    return AltCodingSequence

#added 2 Jan 2021
#This just counts how many different mutations were generated. It splits the input and output sequence into lists, then compares each item (nucleotide) in the list one-by-one and increases a counter if they are the same.
def SameChecker(InputSeq, OutputSeq):
    SameTally = 0
    def split(word):
        return [char for char in word]
    InputSeq=split(InputSeq)
    OutputSeq=split(OutputSeq)

    for i in range(len(InputSeq)):
        if InputSeq[i] == OutputSeq[i]:
            SameTally = SameTally + 1
    return SameTally

