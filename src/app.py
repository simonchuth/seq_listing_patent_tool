import math
import base64
import uuid
import pickle
import re
import json

import streamlit as st
import pandas as pd

from parameters import valid_nucleotide
from sample_data import sample_dict


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def seq_row(seq_chunk):
    chunklist = [seq_chunk[x:x + 10] for x in range(0, len(seq_chunk), 10)]
    seq_chunk_separated = ' '.join(chunklist)
    return seq_chunk_separated


def check_invalid_seq(seq, mod_dict=None, seq_type='DNA'):

    seq_type = seq_type.lower()

    if (seq_type == 'dna') or (seq_type == 'rna'):
        valid_set = valid_nucleotide.copy()

    if mod_dict is not None:
        mod_set = set(mod_dict.keys())
        valid_set = valid_set.union(mod_set)

    for i, char in enumerate(seq):
        if char not in valid_set:
            return [i, char]

    return None


def process_mod(mod):
    if mod != 'nan':
        mod_list = mod.split(';')
        mod_dict = {}
        for mod_entry in mod_list:
            mod_entry = mod_entry.split('=')
            mod_dict[mod_entry[0].strip(' ')] = mod_entry[1].strip(' ')
        return mod_dict

    else:
        return None

def check_nan(display_idx, dict_str):
    for key, val in dict_str.items():
        if val == 'nan':
            st.warning(f'Sequence in row {display_idx} contain missing value \
                for {key}')


def check_cds(display_idx, cds):
    if cds  != 'nan':
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

st.title('Sequence Listing Tool')

app_name = st.text_input('Applicant Name')

inv_title = st.text_input('Title of Invention')

file_ref = st.text_input('File Reference')

df = pd.DataFrame(sample_dict)
tmp_download_link = download_link(df,
                                  'template.csv',
                                  'Template file for sequence listing')
st.markdown(tmp_download_link, unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file", type=['csv'])

if uploaded_file is not None:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

seq_list = df['Sequence'].tolist()
type_list = df['Sample_Type'].tolist()
org_list = df['Organism'].tolist()
cds_list = df['CDS_Range'].tolist()
mod_list = df['Modified_Legend'].tolist()

num_entry = len(seq_list)

output_str ='                         SEQUENCE LISTING\n \n'

if st.button('Generate sequence listing in txt'):
    output_str = add_line(output_str, app_name, num_id=110, num_blank_lines=1)
    output_str = add_line(output_str, inv_title, num_id=120, num_blank_lines=1)
    output_str = add_line(output_str, file_ref, num_id=130, num_blank_lines=1)
    output_str = add_line(output_str, num_entry, num_id=160, num_blank_lines=1)

    for idx in range(num_entry):
        display_idx = idx + 1
        seq = str(seq_list[idx])
        seq_type = str(type_list[idx])
        org = str(org_list[idx])
        cds = str(cds_list[idx])
        mod = str((mod_list[idx]))

        check_nan(display_idx, {'Sequence': seq,
                                'Sequence Type': seq_type,
                                'Organism': org})

        cds = check_cds(display_idx, cds)

        mod_dict = process_mod(mod)

        seq = seq.replace(' ', '').lower()
        invalid_seq_status = check_invalid_seq(seq, mod_dict=mod_dict, seq_type=seq_type)
        if invalid_seq_status is not None:
            st.warning(f'Sequence in row {display_idx} contain invalid \
                character ({invalid_seq_status[1]}) at position \
                ({invalid_seq_status[0]})')
        
        seq_len = len(seq)

        output_str = add_line(output_str, display_idx, num_id=210, num_blank_lines=0)
        output_str = add_line(output_str, seq_len, num_id=211, num_blank_lines=0)
        output_str = add_line(output_str, seq_type, num_id=212, num_blank_lines=0)
        output_str = add_line(output_str, org, num_id=213, num_blank_lines=1)

        if mod_dict is not None:
            for key, feature in mod_dict.items():
                for i, char in enumerate(seq):
                    if char == key:
                        location = i + 1
                        output_str = add_line(output_str, '', num_id=220, num_blank_lines=0)
                        output_str = add_line(output_str, 'misc_feature', num_id=221, num_blank_lines=0)
                        output_str = add_line(output_str, f'({location})..({location})', num_id=222, num_blank_lines=0)
                        output_str = add_line(output_str, f'n = {feature}', num_id=223, num_blank_lines=1)
                seq = seq.replace(key, 'n')

        output_str = add_line(output_str, display_idx, num_id=400, num_blank_lines=0)

        chunk_seq_list = [seq[x:x + 60] for x in range(0, seq_len, 60)]

        for i, seq_chunk in enumerate(chunk_seq_list):
            seq_chunk_separated = seq_row(seq_chunk)
            chunk_len = len(seq_chunk)
            line_count = chunk_len + i * 60
            line_count_str = str(line_count)
            pad_len = 74 - len(seq_chunk_separated) - len(line_count_str)
            pad = ' ' * pad_len
            line_output = seq_chunk_separated + pad + line_count_str
            output_str = add_line(output_str, line_output, num_id=None, num_blank_lines=1)
        output_str = add_line(output_str, '', num_id=None, num_blank_lines=0)

    tmp_download_link = download_link(output_str,
                                      'Sequence_listing.txt',
                                      'Click here to download your sequence listing!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)




