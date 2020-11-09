import streamlit as st
import pandas as pd

from sample_data import sample_dict

from check import check_invalid_seq, check_nan, check_cds

from utils import process_mod, convert_aa_1char_3char
from utils import download_link

from output import add_line
from output import add_nucleotide_no_cds
from output import add_nucleotide_with_cds
from output import add_amino_acid
from output import add_other_info


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
info_list = df['Other_Information'].tolist()

num_entry = len(seq_list)

output_str = '                         SEQUENCE LISTING\n \n'

if st.button('Generate sequence listing in txt'):
    output_str = add_line(output_str, app_name, num_id=110, num_blank_lines=1)
    output_str = add_line(output_str, inv_title, num_id=120, num_blank_lines=1)
    output_str = add_line(output_str, file_ref, num_id=130, num_blank_lines=1)
    output_str = add_line(output_str, num_entry, num_id=160, num_blank_lines=1)

    for idx in range(num_entry):
        display_idx = idx + 1
        seq = str(seq_list[idx])
        seq_type = str(type_list[idx]).upper()
        org = str(org_list[idx])
        cds = str(cds_list[idx])
        mod = str(mod_list[idx])
        info = str(info_list[idx])

        check_nan(display_idx, {'Sequence': seq,
                                'Sequence Type': seq_type,
                                'Organism': org})

        cds = check_cds(display_idx, cds)

        mod_dict = process_mod(mod)

        if (seq_type == 'DNA') or (seq_type == 'RNA'):
            seq = seq.replace(' ', '').lower()
            others_code = 'n'
            others_output = 'n'
        elif (seq_type == 'PRT_1') or (seq_type == 'PRT'):
            others_output = 'Xaa'
            others_code = 'X'
        else:
            st.warning(f'Sequence type in row {display_idx} ({seq_type}) \
                         is unknown')

        invalid_seq_status = check_invalid_seq(seq,
                                               mod_dict=mod_dict,
                                               seq_type=seq_type)
        if invalid_seq_status is not None:
            st.warning(f'Sequence in row {display_idx} contain invalid \
                character ({invalid_seq_status[1]}) at position \
                ({invalid_seq_status[0]})')

        seq_len = len(seq)

        output_str = add_line(output_str,
                              display_idx,
                              num_id=210,
                              num_blank_lines=0)
        output_str = add_line(output_str,
                              seq_len,
                              num_id=211,
                              num_blank_lines=0)
        output_str = add_line(output_str,
                              seq_type[:3],
                              num_id=212,
                              num_blank_lines=0)
        output_str = add_line(output_str,
                              org,
                              num_id=213,
                              num_blank_lines=1)

        if info != 'nan':
            output_str = add_other_info(output_str, info)

        if mod_dict is not None:
            for key, feature in mod_dict.items():
                for i, char in enumerate(seq):
                    if char == key:
                        location = i + 1
                        output_str = add_line(output_str,
                                              '',
                                              num_id=220,
                                              num_blank_lines=0)
                        output_str = add_line(output_str,
                                              'misc_feature',
                                              num_id=221,
                                              num_blank_lines=0)
                        output_str = add_line(output_str,
                                              f'({location})..({location})',
                                              num_id=222,
                                              num_blank_lines=0)
                        output_str = add_line(output_str,
                                              f'{others_output} = {feature}',
                                              num_id=223,
                                              num_blank_lines=1)
                seq = seq.replace(key, others_code)

        output_str = add_line(output_str,
                              display_idx,
                              num_id=400,
                              num_blank_lines=0)

        if seq_type == 'PRT_1':
            seq_type = 'PRT'
            seq = convert_aa_1char_3char(seq)

        if (seq_type == 'DNA') or (seq_type == 'RNA'):
            if cds is None:
                output_str = add_nucleotide_no_cds(display_idx,
                                                   seq,
                                                   output_str)
            else:
                output_str = add_nucleotide_with_cds(display_idx,
                                                     seq,
                                                     output_str,
                                                     cds)
        elif seq_type == 'PRT':
            output_str = add_amino_acid(display_idx, seq, output_str)

    tmp_download_link = download_link(output_str,
                                      'Sequence_listing.txt',
                                      'Download your sequence listing')
    st.markdown(tmp_download_link, unsafe_allow_html=True)
