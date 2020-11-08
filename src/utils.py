import base64
import pandas as pd
from parameters import aa_1char_3char_dict


def seq_row(seq_chunk, segment_len=10):
    chunklist = [seq_chunk[x:x + segment_len]
                 for x in range(0, len(seq_chunk), segment_len)]
    seq_chunk_separated = ' '.join(chunklist)
    return seq_chunk_separated


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


def convert_aa_1char_3char(aa_1char):
    aa_1char = aa_1char.upper()
    aa_3char = [aa_1char_3char_dict[char] for char in aa_1char]
    aa_3char_seq = ' '.join(aa_3char)
    return aa_3char_seq


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. txt_out.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')

    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" \
              download="{download_filename}">{download_link_text}</a>'
