import streamlit as st
from parameters import valid_nucleotide, valid_aa, aa_1char_3char_dict


def check_invalid_seq(seq, mod_dict=None, seq_type='DNA'):

    if (seq_type == 'DNA') or (seq_type == 'RNA'):
        valid_set = valid_nucleotide.copy()
    elif (seq_type == 'PRT'):
        valid_set = valid_aa.copy()
        seq = seq.split(' ')
    elif seq_type == 'PRT_1':
        valid_set = set(aa_1char_3char_dict.keys())

    if mod_dict is not None:
        mod_set = set(mod_dict.keys())
        valid_set = valid_set.union(mod_set)

    for i, element in enumerate(seq):
        if element not in valid_set:
            return [i, element]

    return None


def check_nan(display_idx, dict_str):
    for key, val in dict_str.items():
        if val == 'nan':
            st.warning(f'Sequence in row {display_idx} contain missing value \
                for {key}')


def check_cds(display_idx, cds):
    if cds != 'nan':
        cds_split = cds.split(',')
        if len(cds_split) != 2:
            st.warning(f'CDS_Range in row {display_idx} is of incorrect \
                format ({cds}), it should be 2 numbers separated by a comma.\
                 e.g. 21,51')
            return None

        start = int(cds_split[0])
        end = int(cds_split[1])
        CDS_len = end - start + 1
        if CDS_len % 3 != 0:
            st.warning(f'CDS_Range in row {display_idx} is invalid. The range \
                should be in multiple of 3, {start} to {end} is not in \
                multiple of 3')
            return None

        return [start, end]

    else:
        return None


def check_valid_codon(display_idx, codon, position='first'):
    codon = codon.lower()
    codon = codon.replace('u', 't')
    if position == 'first':
        if codon != 'atg':
            st.warning(f'Row {display_idx}: The first codon ({codon}) \
                        is not ATG/AUG. Is there a mistake?')
        return True

    elif position == 'last':
        if (
            (codon == 'tag')
            or (codon == 'taa')
            or (codon == 'tga')
           ):

            st.warning(f'Row {display_idx}: No need to include the \
                        termination codon')
            return False
        return True


def check_cds_region(display_idx, cds_region):
    seq_len = len(cds_region)
    if seq_len < 3:
        st.warning(f'Row {display_idx}: Sequence length of CDS region is \
                     too short')
    else:
        first_codon = cds_region[:3]
        last_codon = cds_region[-3:]
        check_valid_codon(display_idx, first_codon, position='first')
        if not check_valid_codon(display_idx, last_codon, position='last'):
            cds_region = cds_region[:-3]

    return cds_region