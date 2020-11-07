import numpy as np

sample_seq = ['ATCATGATGCGATGCTA1CAA2GATCA@GATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATGAATCATGATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGGCAGGGCGATGAAGATCGATCG',
              'AUGCGUACATGCGAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATTGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATGUACGUAC',
              'Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met Ala Cys Asp Glu Phe Gly His Ile Lys Leu Met',
              'TYAGVLYERDVLYERGVLYERDYERGV',
              'TYAG!VL@YER#DVLYERGVLYERDYERGV']
sample_type = ['DNA','RNA', 'PRT', 'PRT_1', 'PRT_1']
sample_org = ['Homo sapiens', 'Homo sapiens', 'Homo sapiens', 'Homo sapiens', 'Homo sapiens']
sample_cds = [np.nan, '25, 51', np.nan, np.nan, np.nan]
sample_mod = ['1=ABC; 2=DEF; @=XYZ or ABC', np.nan, np.nan, np.nan, '!=Positive amino acid; @=Negative amino acid; #=Hydrophobic amino acid']
sample_dict = {'Sequence': sample_seq,
               'Sample_Type': sample_type,
               'Organism': sample_org,
               'CDS_Range':sample_cds,
               'Modified_Legend': sample_mod
               }