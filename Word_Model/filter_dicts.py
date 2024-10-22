"""
filter_dicts.py  -v VOCAB_LIST  -o OUTPUT_DICT -d DICT_1 DICT_2 .... DICT_N

Takes each of the N dictionaries and filters for the words in VOCAB_LIST
and outputs them to the OUTPUT_DICT file

VOCAB_LIST is a line-separated file with one word per line
DICT_I is a tab seperated dictionary in format word\tentry
OUTPUT_DICT will be a tab separated dictionary in format word\tentry
"""

import argparse
import pandas as pd
import re

def configure_arguments(parser):
    parser.add_argument('-v','--vocab_file')
    parser.add_argument('-o','--output_file')
    parser.add_argument('-d','--dictionary_files', nargs='+')

def normalize(word):
    return re.sub(' ','-',word).lower()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    with open(args.vocab_file,'r') as fp:
        words = fp.read().split('\n')
        words = map(lambda s: re.sub('\r','',s).lower(), words)

    word_id = {w:i for (i, w) in enumerate(words)}

    words_df = pd.DataFrame([])
    for dfp in args.dictionary_files:
        df = pd.read_csv(dfp, sep = '\t', na_filter=False, header = None,
            names = ['word','entry'])
        df['word'] = df['word'].map(normalize)
        df = df[df['word'].isin(word_id)]
        words_df = words_df.append(df, ignore_index= True)
        print('Filtered dictionary:',dfp)
        print('Number of Entries:',df.shape[0])

    words_df.to_csv(args.output_file, sep ='\t', index = False, headers= False)

# List of Dictionaries to Use:
