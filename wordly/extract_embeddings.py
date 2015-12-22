"""
extract_embeddings -v VOCAB_LIST -o OUT_FILE [ -url WORD2VEC_API ] 

Takes each entry of words and looks up their corresponding embedding
"""

import requests
import numpy
import argparse
import base64
import h5py
import re

def configure_arguments(parser):
    parser.add_argument('-v','--vocab_file')
    parser.add_argument('-o','--output_file')
    parser.add_argument('-url','--url_api',
        default = 'http://127.0.0.1:5000/word2vec/model?word=')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    print 'Reading vocab file', args.vocab_file
    with open(args.vocab_file,'r') as fp:
        words = fp.read().split('\n')
        words = map(lambda s: re.sub('\r','',s).lower(), words)

    num_words = len(words)
    embed_size = 300            # Static for now - only using Google's
    base_url = args.url_api

    embeddings = numpy.zeros((1,embed_size))
    final_words = ['<UNK>']
    print 'Fetching embeddings..'
    for word in words:

        url = base_url + word

        r = requests.get(url)
        v_64 = r.json()

        if v_64 is None:
            continue

        # Decode Embedding
        v_decode = base64.b64decode(v_64)
        v = numpy.fromstring(v_decode,dtype=numpy.float32)

        # Store the embedding and word
        embeddings = numpy.append(embeddings,[v], axis = 0)
        final_words.append(word)
        if len(final_words) % 1000 == 0:
            print 'Processed embedding for', word

    print 'Found embeddings for %d words' % len(final_words)
    print 'Saving embeddings to', args.output_file

    h5f = h5py.File(args.output_file,'w')
    h5f.create_dataset('words', data = final_words)
    h5f.create_dataset('embeddings', data = embeddings)
    h5f.close()
