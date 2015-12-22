from keras.models import model_from_json
from process_data import sen_to_idx, padd_sentence, get_sentence_embeddings
from operator import itemgetter
from itertools import izip, islice
import h5py
import pickle

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

import theano.tensor as T
import numpy

def print_v(verbose, *args):
    if verbose:
        print(args)

class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance

class Wordly(Singleton):
    """
    Wordly API for the webapp to decide on predictions for a user's query

    Wordly implements a Singleton design. There can only be one true instance
    in an environment

    Note: The Wordly instance needs to be initialized using INITIALZIE_MODE()
        before being able to make any predictions
    """
    def __init__(self, maxlen = 20, embedsize = 64):
        self.maxlen = maxlen
        self.embedsize = embedsize

        self.tokens = {"<UNK>": 0, "<S>": 1, "</S>":2, "<PAD>": 3}

    # def get_instance(self):
    #     return self._instance

    def get_model(self, json = 'model.json', maxlen = 20, embedsize = 64):
        # @Note: Model_from_json currently does not work
        # model = model_from_json(json_string)
        # Compiling the graph from static implementation

        model = Sequential()
        model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, embedsize)))
        model.add(Dropout(0.2))
        model.add(LSTM(512, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(embedsize, init='glorot_normal'))
        model.add(Activation('linear'))

        return model        

    def initialize_model(self, json = 'model.json', 
        weights = 'weights.hdf5',
        embed_path = 'embeddings.hdf5', verbose = False):
        def euclidian_dist(y_true,y_pred):
            return T.sqrt(T.sum((y_true - y_pred) ** 2, axis = 1))

        json_string = json

        # JSON is a file
        if json.endswith('.json'):
            with open(json,'r') as fp:
                json_string = fp.read()

        # Build Model
        print_v(verbose, '[LOG] Compiling Model...')
        model = self.get_model(json, self.maxlen, self.embedsize)
        model.load_weights(weights)
        model.compile(loss=euclidian_dist, optimizer='rmsprop')

        self.model = model 

        # Initalize Embeddings
        print_v(verbose, '[LOG] Loading Embeddings...')

        if embed_path.endswith('.pkl'):
            with open(embed_path,'r') as pkl:
                words, embeddings = pickle.load(pkl)
        elif embed_path.endswith('.hdf5'):
            with h5py.File(embed_path,'r') as h5f:
                words = h5f['words'][:]
                embeddings = h5f['embeddings'][:]

        self.word_id = {w:i for (i, w) in enumerate(words)}
        self.id_word = dict(enumerate(words))
        self.embeddings = embeddings

    @staticmethod
    def k_nearest(e, embeddings, k):
        """Sorts words according to their Euclidean distance.
           To use cosine distance, embeddings has to be normalized so 
           that their l2 norm is 1."""
        e = e
        distances = (((embeddings - e) ** 2).sum(axis=1) ** 0.5)
        sorted_distances = sorted(enumerate(distances), key=itemgetter(1))
        return zip(*sorted_distances[:k])

    @staticmethod
    def knn(word, id_word, embeddings, k = 5, verbose = False):
        """
        Finds the K-nearest neighbors to the vector WORD in the vocabulary

        :returns A tuple with the list of neighbors and list of distances
        """
        indices, distances = Wordly.k_nearest(word, embeddings, k)
        neighbors = [id_word[idx] for idx in indices]
        if verbose:
            for i, (word, distance) in enumerate(izip(neighbors, distances)):
                print(i, '\t', word, '\t\t', distance)
        return (neighbors,distances)

    def look_up(self, query, k = 5, verbose = False):
        """
        Takes a string QUERY and embeds each word in the embedding space
        then uses the RNN model to predict a dictionary entry.

        The predicted entry is then compared against its K closest neighbors
        Look up returns a list of possible entries in decreasing confidence 
        (taken as Euclidean distance)
        """
        # self.tokens = {"<UNK>": 0, "<S>": 1, "</S>":2, "<PAD>": 3} 

        idx = sen_to_idx(query, self.word_id)
        idx = padd_sentence(idx, self.maxlen, self.tokens, 
            include_sens_tags = True)
        matrix = numpy.reshape(list(idx), (1, self.maxlen))
        # print matrix

        definition = get_sentence_embeddings(matrix, self.embeddings)
        definition = numpy.reshape(definition, (1, self.maxlen, self.embedsize))
        # print 'Definition:', definition

        pred = self.model.predict(definition, verbose = int(verbose))
        # print 'Prediction', pred
        neighbors, distance = self.knn(pred, self.id_word, self.embeddings, 
            k, verbose = verbose)
        # return (definition, pred)
        return zip(neighbors, distance)

    def get_embeddings(self):
        return self.embeddings

        
