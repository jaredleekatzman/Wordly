"""
process_data.py -v VOCAB_EMBEDDING_FILE -d DICTIONARY_FILE -o OUTPUT_FILE 
                --timestamp TRUE|FALSE --embeddings TRUE|FALSE --max_len N

This Script should take in a dictionary in the format of:
word\tdefinition
And based on the vocabulary list where the index of the word is its ID:
convert the words and definitions to a dataset of X, y
Based on a flag: embedding
Return either the embeddings or the index matrix

Author: Jared Katzman (12/18/2015)
"""
import argparse
import pickle, cPickle
import pandas as pd
import re
from datetime import datetime

SUCCESS = 0
FAILURE = 1

def configure_arguments(parser):
    parser.add_argument('-v','--vocab_file')
    parser.add_argument('-d','--dictionary_file')
    parser.add_argument('-o','--output_file')
    parser.add_argument('-t','--timestamp', type=bool, default=True)
    parser.add_argument('-e','--embeddings', type=bool, default=True)
    parser.add_argument('-ml''--max_len',type=int, default=20)

def case_normalizer(word, dictionary):
    """ In case the word is not available in the vocabulary,
     we can try multiple case normalizing procedure.
     We consider the best substitute to be the one with the lowest index,
     which is equivalent to the most frequent alternative."""
    w = word
    lower = (dictionary.get(w.lower(), 1e12), w.lower())
    upper = (dictionary.get(w.upper(), 1e12), w.upper())
    title = (dictionary.get(w.title(), 1e12), w.title())
    results = [lower, upper, title]
    results.sort()
    index, w = results[0]
    if index != 1e12:
        return w
    return word

def normalize(word, word_id):
    """ Find the closest alternative in case the word is OOV.
    Returns the index of the word
    """
    # Noramlize digits by replacing them with #
    DIGITS = re.compile("[0-9]", re.UNICODE)

    if not word in word_id:
        word = DIGITS.sub("#", word)
    if not word in word_id:
        word = case_normalizer(word, word_id)

    if not word in word_id:
        return None
    return word

def sen_to_idx(sentence, word2id):
    """
    Function that takes a dictionary entry and word and maps 
    it to the given vocab list word2id
    """
    if isinstance(sentence,list):
        return map(lambda s: sen_to_idx(s, word2id), sentence)
    
    # Remove punctuation and split sentence into words
    sentence = re.sub(r'[^\w\s]','',sentence) 
    words = sentence.split(' ')
    
    # Normalize Each Word
    words = map(lambda w: normalize(w, word2id), words)
    
    # Assumes 0 is the <UNK> token
    idx = [word2id.get(word, 0) for word in words]
    return idx

def get_sentence_embeddings(sent, embeddings):
    """
    Takes a matrix of sent (NUM_SENT, MAXLEN)
    and embeddings (NUM_WORDS, EMBED_SIZE)
    Map each word of each sentence to its emebeddings 
    """
    num_sent, maxlen = sent.shape
    num_words, embed_size = embeddings.shape
    sen_embed = np.zeros((num_sent, maxlen, embed_size))
    for i in range(num_sent):
        for j in range(maxlen):
            sen_embed[i,j,:] = embeddings[sent[i,j]]

    return sen_embed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    if args.timestamp:
        strtime = datetime.now().strftime("%d%m_%M%S")
        args.output_file = strtime + args.output_file

    # Open Vocab List and Embeddings
    if args.vocab_file.endswith('.pkl'):
        words, embeddings = pickle.load(open(args.vocab_file, 'rb'))
    else:
        raise ValueError('File type not supported for given vocab_file %s' 
            % args.vocab_file)

    # Map words to indices and vice versa
    word_id = {w:i for (i, w) in enumerate(words)}
    id_word = dict(enumerate(words))

    # Open Dictionary File
    with open(args.dictionary_file,'r') as dfp:
       df = pd.read_csv(dfp, sep = '\t', na_filter=False)

    # Map entries and words to their IDs in vocab list WORDS
    idx = df['entry'].map(lambda s: sen_to_idx(s, word_id))
    y_idx = df['word'].map(lambda w: word_id.get(normalize(w, word_id), 0))
    if not args.embeddings:
        pdf = pd.concat([y_idx, idx], axis = 1)
        pdf.to_csv(args.output_file, sep ='\t')
        return SUCCESS

    # Add Padding and Start / End TOKENS
    x_idx = padd_sentence(idx, maxlen)
    x_idx = np.asarray(list(locs)) # Convert pd.Series to np.Array
    X = get_sentence_embeddings(x_idx, embeddings)

    y = map(lambda i: embeddings[i], y_idx.values)
    y = np.asarray(Y)

    if args.output_file.endswith('.pkl'):
        with open(args.output_file,'w') as output:
            cPickle.dump((X,y),output, -1) # -1 = cPickle.HIGHEST_PROTOCOL
    elif args.output_file.endswith('.h5'):
        h5f = h5py.File(args.output_file,'w')
        h5f.create_dataset('X', data = X)
        h5f.create_dataset('y', data = y)
        h5f.close()

    return SUCCESS
