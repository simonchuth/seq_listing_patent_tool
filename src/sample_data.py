import numpy as np

sample_seq = ['ATCATGATGCGATGCTA1CAA2GATCA@GATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATGAATCATGATGCGATGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGGCAGGGCGATGAAGATCGATCG',
              'AUGCGUACATGCGAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATTGCTAGCAATGCGATGCTAGCATGACGGCAGGGCGATGAAGACGATGCTAGCATGUACGUAC']
sample_type = ['DNA','RNA']
sample_org = ['Homo sapiens', 'Homo sapiens']
sample_cds = [np.nan, '25, 51']
sample_mod = ['1=ABC; 2=DEF; @=XYZ or ABC', np.nan]
sample_dict = {'Sequence': sample_seq,
               'Sample_Type': sample_type,
               'Organism': sample_org,
               'CDS_Range':sample_cds,
               'Modified_Legend': sample_mod
               }