from keras.models import model_from_json


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

    def sen_to_idx(sentence, word2id):
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

    def padd_sentence(sent, maxlen, tokens, include_sens_tags = False):
        """
        Takens an individual sentence SENT
        Padds it with PADD to the specified MAXLEN
        """
        tags = 2 * int(include_sens_tags)
        if len(sent) > (maxlen - tags):
            sent = sent[:(maxlen - tags)]

        if include_sens_tags:
            sent = [tokens['<S>']] + sent + [tokens['</S>']]

        sent = sent + [tokens['<PAD>']] * (maxlen - len(sent))
        return sent

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

    def look_up(query, k = 5):


        
