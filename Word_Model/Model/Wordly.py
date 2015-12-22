from keras.models import model_from_json
from process_data import sen_to_idx, padd_sentence, get_sentence_embeddings
from operator import itemgetter
from itertools import izip, islice

class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance


class Wordly(Singleton):
    
    def __init__(self, maxlen = 20, embedsize = 64):
        self.maxlen = maxlen
        self.embedsize = embedsize

    def get_instance(self):
        return self._instance

    def get_model(self, maxlen = 20, embedsize = 64):
        model = Sequential()
        model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, embedsize)))
        model.add(Dropout(0.2))
        model.add(LSTM(512, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(embedsize, init='glorot_normal'))
        model.add(Activation('linear'))
        model.load_weights(weights)

        return model        

    def initialize_model(self, json = 'model.json', 
        weights = 'weights.hdf5',
        embed_path = 'embeddings.'):
        def euclidian_dist(y_true,y_pred):
            return T.sqrt(T.sum((y_true - y_pred) ** 2, axis = 1))

        json_string = json

        # JSON is a file
        if json.endswith('.json'):
            with open(json,'r') as fp:
                json_string = fp.read()

        # Build Model
        # Model_from_json currently does not work
        # model = model_from_json(json_string)
        model = self.get_model(self.maxlen, self.embedsize)

        model.compile(loss=euclidian_dist, optimizer='rmsprop')
        self.model = model 

        # Initalize Embeddings
        with h5py.File(embed_path,'r') as h5f:
            words = h5f['words'][:]
            embeddings = h5f['embeddings'][:]

        self.word_id = {w:i for (i, w) in enumerate(words)}
        self.id_word = dict(enumerate(words))
        self.embeddings = embeddings

    def k_nearest(self, e, k):
        """Sorts words according to their Euclidean distance.
           To use cosine distance, embeddings has to be normalized so 
           that their l2 norm is 1."""
        e = e
        distances = (((self.embeddings - e) ** 2).sum(axis=1) ** 0.5)
        sorted_distances = sorted(enumerate(distances), key=itemgetter(1))
        return zip(*sorted_distances[:k])

    def knn(self, word, k = 5, verbose = False):
        indices, distances = k_nearest(word, k)
        neighbors = [self.id_word[idx] for idx in indices]
        if verbose:
            for i, (word, distance) in enumerate(izip(neighbors, distances)):
                print(i, '\t', word, '\t\t', distance)
        return (neighbors,distance)

    def look_up(query, k = 5, verbose = False):
        idx = sen_to_idx(query, self.word_id, self.maxlen)
        matrix = numpy.asarray(list(idx))
        definition = get_sentence_embeddings(matrix, self.embeddings)

        pred = self.model.predict(definition, verbose = int(verbose))

        neighbors, distance = knn(pred, k, verbose = verbose)
        return izip(neighbors, distance)

        
