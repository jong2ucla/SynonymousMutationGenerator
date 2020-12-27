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
    'AGA':'R',  'AGG':'R',  'TAA':'***',  'TAG':'***',  'TGA':'***'}

#Now, I'll tackle the input sequence in chunks of three and substitute each codon for its amino acid.
    Protein =""
    for i in range (0,len(NucleotideSequence),3):
        codon = NucleotideSequence[i:i + 3]
        Protein += NucCodonDict[codon]
    return Protein

#Next, I'll use a similar method to substitute each codon for its synonymous codon.
def AltCodon(UserSeq):

    ##This is my dictionary for the best alternative codon (using human codon frequency).
    ##Best alternative codon was determined in this manner, with the higher numbered items taking higher priority:
    ##(1) The alternative codon codes for the same amino acid as the original codon (no alternative codons given for Met, Trp, or stop codons [-Term])
    ##(2) The most nucleotides was changed to generate the alternative codon (eg, for Leu, CTT was changed to TTG, not CTC)
    ##(3) The alternative codon was chosen to have the highest frequency of the remaining codons
    ##(4) Wobble base pairing was avoided. In particular, in the third position of the codon, A to G mutations and C to T mutations were avoided. A codon of lesser frequency was chosen in this case.

    HumanAltCodonDict={'ATT':'ATC',   'ATC':'ATA',  'ATA':'ATC',  'CTT':'TTG',  'CTC':'CTG',
    'CTA':'TTA',  'CTG':'CTC',  'TTA':'CTA',  'TTG':'CTT',  'GTT':'GTA',  'GTC':'GTG',
    'GTA':'GTT',  'GTG':'GTC',  'TTT':'TTC',  'TTC':'TTT',  'ATG':'ATG',  'TGT':'TGC',
    'TGC':'TGT',  'GCT':'GCA',  'GCC':'GCA',  'GCA':'GCC',  'GCG':'GCC',  'GGT':'GGA',
    'GGC':'GGA',  'GGA':'GGC',  'GGG':'GGC',  'CCT':'CCA',  'CCC':'CCA',  'CCA':'CCC',
    'CCG':'CCC',  'ACT':'ACA',  'ACC':'ACA',  'ACA':'ACC',  'ACG':'ACC',  'TCT':'AGC',
    'TCC':'AGC',  'TCA':'AGC',  'TCG':'AGC',  'AGT':'TCC',  'AGC':'TCC',  'TAT':'TAC',
    'TAC':'TAT',  'TGG':'TGG',  'CAA':'CAG',  'CAG':'CAA',  'AAT':'AAC',  'AAC':'AAT',
    'CAT':'CAC',  'CAC':'CAT',  'GAA':'GAG',  'GAG':'GAA',  'GAT':'GAC',  'GAC':'GAT',
    'AAA':'AAG',  'AAG':'AAA',  'CGT':'CGG',  'CGC':'AGA',  'CGA':'AGA',  'CGG':'AGA',
    'AGA':'CGC',  'AGG':'CGG',  'TAA':'***',  'TAG':'***',  'TGA':'***'}

#Now, I'll tackle the input sequence in chunks of three and substitute each input codon for its synonymous, alternative codon.
    AltCodingSequence =""
    for i in range (0,len(UserSeq),3):
        codon = UserSeq[i:i + 3]
        AltCodingSequence += HumanAltCodonDict[codon]
    return AltCodingSequence
