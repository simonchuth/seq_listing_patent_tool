from parameters import params, codon_dict
from utils import seq_row
from check import check_cds_region
import streamlit as st


def add_aa_list(output_str, segment_aa_list, aa_count):
    # amino acid line
    aa_line_output = ' '.join(segment_aa_list)
    output_str = add_line(output_str,
                          aa_line_output,
                          num_id=None,
                          num_blank_lines=0)

    # amino acid position line
    aa_count_line_output = ''
    for i, aa in enumerate(segment_aa_list):
        aa_count += 1
        if (aa_count == 1) or (aa_count % 5 == 0):
            str_aa_count = str(aa_count)
            pad_len = 3 - len(str_aa_count)
            pad = ' ' * pad_len
            aa_count_line_output += pad + str_aa_count + ' '
        else:
            aa_count_line_output += ' ' * 4
    output_str = add_line(output_str,
                          aa_count_line_output,
                          num_id=None,
                          num_blank_lines=1)

    return output_str, aa_count


def add_nucleotide_no_cds(display_idx,
                          seq,
                          output_str,
                          extra_line_break=True,
                          last_nn_count=0):
    seq_len = len(seq)
    chunk_seq_list = [seq[x:x + 60] for x in range(0, seq_len, 60)]

    for i, seq_chunk in enumerate(chunk_seq_list):
        seq_chunk_separated = seq_row(seq_chunk, segment_len=10)
        chunk_len = len(seq_chunk)
        line_count = last_nn_count + chunk_len + i * 60
        line_count_str = str(line_count)
        content_len = len(seq_chunk_separated) + len(line_count_str)
        pad_len = params['line_width'] - content_len
        pad = ' ' * pad_len
        line_output = seq_chunk_separated + pad + line_count_str
        output_str = add_line(output_str,
                              line_output,
                              num_id=None,
                              num_blank_lines=1)

    if extra_line_break:
        output_str = add_line(output_str,
                              '',
                              num_id=None,
                              num_blank_lines=0)

    return output_str


def add_nucleotide_with_cds(display_idx, seq, output_str, cds):
    b4_cds = seq[:cds[0] - 1]
    aft_cds = seq[cds[1]:]
    cds_region = seq[cds[0] - 1: cds[1]]

    if len(b4_cds) > 0:
        output_str = add_nucleotide_no_cds(display_idx,
                                           b4_cds,
                                           output_str,
                                           extra_line_break=False)

    aa_count = 0
    seq_len = len(cds_region)

    cds_region = check_cds_region(display_idx, cds_region)

    chunk_seq_list = [cds_region[x:x + 48] for x in range(0, seq_len, 48)]
    for i, seq_chunk in enumerate(chunk_seq_list):
        if len(seq_chunk) == 0:
            break
        seq_chunk_separated = seq_row(seq_chunk, segment_len=3)
        chunk_len = len(seq_chunk)
        line_count = chunk_len + i * 48 + len(b4_cds)
        line_count_str = str(line_count)
        content_len = len(seq_chunk_separated) + len(line_count_str)
        pad_len = params['line_width'] - content_len
        pad = ' ' * pad_len
        line_output = seq_chunk_separated + pad + line_count_str
        output_str = add_line(output_str,
                              line_output,
                              num_id=None,
                              num_blank_lines=0)

        # output for amino acid
        codon_list = seq_chunk_separated.split(' ')

        try:
            segment_aa_list = [codon_dict[codon.replace('u', 't')]
                               for codon in codon_list]
        except KeyError:
            st.warning(f'Row {display_idx}: There are invalid codons  or \
                         termination codon within the CDS region. \
                         {codon_list}')
            continue

        output_str, aa_count = add_aa_list(output_str,
                                           segment_aa_list,
                                           aa_count)

    if len(aft_cds) > 0:
        last_nn_count = len(aft_cds) + len(cds_region)
        output_str = add_nucleotide_no_cds(display_idx,
                                           aft_cds,
                                           output_str,
                                           extra_line_break=True,
                                           last_nn_count=last_nn_count)

    return output_str


def add_amino_acid(display_idx, aa_3char_seq, output_str):
    aa_list = aa_3char_seq.split(' ')
    chunk_aa_list = [aa_list[x:x + 16] for x in range(0, len(aa_list), 16)]

    aa_count = 0
    for i, aa_chunk in enumerate(chunk_aa_list):
        output_str, aa_count = add_aa_list(output_str,
                                           aa_chunk,
                                           aa_count)

    return output_str


def add_line(output_str, content, num_id=None, num_blank_lines=0):
    line_str = ''

    if not isinstance(content, str):
        content = str(content)

    if num_id is not None:
        line_str = line_str + f'<{num_id}>  '

    line_str = line_str + content + ' \n'

    # Add blank lines
    line_str = line_str + ' \n' * num_blank_lines
    output_str = output_str + line_str

    return output_str
