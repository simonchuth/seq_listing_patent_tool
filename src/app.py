import math
import base64
import uuid
import pickle
import re
import json

import streamlit as st
import pandas as pd


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

def process_row(row_text):
    row_text = row_text + '\n'
    return row_text

def seq_row(seq_chunk):
    chunklist = [seq_chunk[x:x + 10] for x in range(0, len(seq_chunk), 10)]
    seq_chunk_separated = ' '.join(chunklist)
    return seq_chunk_separated

def check_invalid_seq(seq):
    seq = seq
    valid_char = set(['a', 't', 'c', 'g', 'u'])
    for i, char in enumerate(seq):
        if char not in valid_char:
            return [i, char]
    return None


st.title('Sequence Listing Tool')

app_name = st.text_input('Applicant Name')

inv_title = st.text_input('Title of Invention')

file_ref = st.text_input('File Reference')

sample_seq = ['ATCGATCGATCG', 'AUGCGUACGUACGUAC']
sample_type = ['DNA','RNA']
sample_org = ['Homo sapiens', 'Homo sapiens']
sample_dict = {'Sequence': sample_seq,
               'Sample Type': sample_type,
               'Organism': sample_org}
df = pd.DataFrame(sample_dict)
tmp_download_link = download_link(df, 'template.csv', 'Template file for sequence listing')
st.markdown(tmp_download_link, unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file", type=['csv'])

if uploaded_file is not None:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

seq_list = df.iloc[:, 0].tolist()
type_list = df.iloc[:, 1].tolist()
org_list = df.iloc[:, 2].tolist()

st.write(df)

num_entry = len(seq_list)

output_str = ''

if st.button('Generate sequence listing in txt'):
    output_str = output_str + process_row('                         SEQUENCE LISTING')
    output_str = output_str + process_row('')
    output_str = output_str + process_row('<110>  ' + app_name)
    output_str = output_str + process_row('')
    output_str = output_str + process_row('<120>  ' + inv_title)
    output_str = output_str + process_row('')
    output_str = output_str + process_row('<130>  ' + file_ref)
    output_str = output_str + process_row('')
    output_str = output_str + process_row('<160>  ' + str(num_entry))
    output_str = output_str + process_row('')
    for idx in range(num_entry):
        display_idx = idx + 1
        seq = seq_list[idx]
        seq = seq.replace(' ', '').lower()
        invalid_seq_status = check_invalid_seq(seq)
        if invalid_seq_status is not None:
            st.warning(f'Sequence in row {display_idx} contain invalid character ({invalid_seq_status[1]}) at position ({invalid_seq_status[0]})')
        seq_len = len(seq)
        seq_type = type_list[idx]
        org = org_list[idx]

        num_seq_row = math.ceil(seq_len / 60)
        chunk_seq_list = [seq[x:x + 60] for x in range(0, seq_len, 60)]

        output_str = output_str + process_row('<210>  ' + str(display_idx))
        output_str = output_str + process_row('<211>  ' + str(seq_len))
        output_str = output_str + process_row('<212>  ' + seq_type)
        output_str = output_str + process_row('<213>  ' + org)
        output_str = output_str + process_row('')
        output_str = output_str + process_row('<400>  ' + str(display_idx))
        for i, seq_chunk in enumerate(chunk_seq_list):
            seq_chunk_separated = seq_row(seq_chunk)
            chunk_len = len(seq_chunk)
            line_count = chunk_len + i * 60
            line_count_str = str(line_count)
            pad_len = 74 - len(seq_chunk_separated) - len(line_count_str)
            pad = ' ' * pad_len
            output_str = output_str + process_row(seq_chunk_separated + pad + line_count_str)
        output_str = output_str + process_row('')

    tmp_download_link = download_link(output_str, 'Sequence_listing.txt', 'Click here to download your sequence listing!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)




