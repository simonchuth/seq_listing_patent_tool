import numpy as np

sample_seq = ['ATCATGATGCGATGCTA1CAA2GATCA@GATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATGAATCATGATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGGCAGGGCGATGAAGATCGATCG',
              'ATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATG',
              'Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met',
              'TYAGVLYERDVLYERGVLYERDYERGV',
              'TYAG!VL@YER#DVLYERGVLYERDYERGV',
              'ATCGATGCATGCATGC',
              'ATGCTGATGCTAGTTCAGTCGTACGCTAGCT']
sample_type = ['DNA','RNA', 'PRT', 'PRT_1', 'PRT_1', 'DNA', 'DNA']
sample_org = ['Homo sapiens', 'Mus musculus', 'Rattus norvegicus', 'Escherichia coli', 'Dengue virus', 'Artificial Sequence', 'Unknown']
sample_cds = [np.nan, '25, 51', np.nan, np.nan, np.nan, np.nan, np.nan]
sample_mod = ['1=ABC; 2=DEF; @=XYZ or ABC', np.nan, np.nan, np.nan, '!=Positive amino acid; @=Negative amino acid; #=Hydrophobic amino acid', np.nan, np.nan]
sample_info = [np.nan, np.nan, np.nan, np.nan, np.nan, 'This is a sample artificial sequence. If this line is longer than the width of the sequence listing, it will just wrap to the next line. If the word is longer than the line width, it will just occupy the whole line like this word Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokaiwhenuaki', 'This is a sample unknown sequence']
sample_dict = {'Sequence': sample_seq,
               'Sample_Type': sample_type,
               'Organism': sample_org,
               'CDS_Range': sample_cds,
               'Modified_Legend': sample_mod,
               'Other_Information': sample_info
               }