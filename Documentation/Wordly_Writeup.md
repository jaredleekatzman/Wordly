# Wordly Reverse Dictionary

**Team Members:** Jared Katzman & Tim Follo

## Abstract

This reverse dictionary makes decision by using the weights computed by the RNN. The RNN 'decided' on these weights by performing thousands of computation to minimize the euclidian distance between a predicted word vector and a definition entry's true value. When the user queries the reverse dictionary, it performs a mathematical operation on the vectorized version of the query. We decide to show the user the X  closest words in vector space, in hopes that one of them is the word the user is thinking of.  

## Design
Numerous algorithms in Natural Language Processing (NLP) compute mathematical representations of words. These representations have shown to encode important semantic relationships and allow for more effective language modeling.

One methodology, *word2vec* [^word2vec], computes vector representations of words such that linear operations have semantic meanings. A common example is:
$$
v(king) - v(man) + v(woman) \approx v(queen) 
$$ 
Where if you subtract the vector representing man from king and then add the vector woman, the result will be close to the representation of queen. 

[^word2vec]: Word2vec is not an actual algorithm but a framework for implementing the vectorization of words. Word2vec models implement either the skip-gram algorithm or Continuous Bag of Words (CBOW). Continuous Bag of Words attempts to predict a word from its context. Meanwhile, the skip-gram algorithm is the reverse; it attempts to predict the context from a given word. Increasing the probability of a word given another word is eqauted with decreasing the distance between these two words in vector space. Training these algorithms over large natural language corpouses can result in vectors that are able to perform semanticaly meaningfuly computations. See Google's [Word2Vec](https://code.google.com/p/word2vec/) for more information.

Examples like this have led us to question the extent of possible operations. Vector embeddings are commonly used in deep learning systems for a multitude of different tasks, for example sentiment analysis [^sent] and learning how to answer questions about written stories [^babi]. We will take these techniques and apply them to a new task: building a reverse dictionary. 

[^sent]: [LSTM Networks for Sentiment Analysis](http://deeplearning.net/tutorial/lstm.html)

[^babi]: [Facebook bAbI project](https://research.facebook.com/researchers/1543934539189348)

The premise is to take the definitions of a dictionary and build a deep neural network that learns to predict the corresponding entry words. We expect the network will learn general enough definitions for words such that a user can query the dictionary with a definition and the reverse dictionary will be able to predict which word the user is thinking of. The overall design of the system is below:

[include graphic]

We will take our training data (a set of definitions and their respective dictionary entries) and compute a vector representation of the words and defintions (a matrix of word vectors). We will then have numerical input for the network. The architecture of the network will be a recurrent neural network. We will train the network on the input data and attempt to minimize the euclidian distance between the predicted word vector and the true dictionary entry. Lastly, we will build a UI 
to allow users to query their own definitions. The system will predict possible dictionary entries and display them to the user.

## Implementation
### Training Data 
We scraped multiple dictionaries to produce an an ecclectic dataset of dictionary entries. The hope was to provide more linguistic diversity for the neural network to train on. The dictionaries we used are the follow:

- Princeton University's WordNet [^wordnet]
- Oxford English Dictionary [^oxford]
- Webster's Unabridged Dictionary [^webster]

[^wordnet]: Princeton University "About WordNet." WordNet. Princeton University. 2010. <http://wordnet.princeton.edu> 

[^oxford]: Oxford Dictionaries. Oxford University Press, n.d. Web. 20 December 2015. <https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt>

[^webster]: Lawrence, Graham, comp. Webster's Unabridged Dictionary. N.p.: Project Gutenberg, 2009. Text file. <https://ia600500.us.archive.org/zip_dir.php?path=/15/items/webstersunabridg29765gut.zip&formats=TEXT>

For ease of training, we capped each of the definitions to 20 words. For defitions that were shorter than 20 words, we right padded them with a special padding token \<PAD\>

### Word Embeddings
Running these algorithms can be very time intensive, so numerous projects have surfaced to provide precalculated embeddings. We utilized the embeddings from the *Polyglot* project [^polyglot].

[^polyglot]: [Polyglot: Distributed Word Representations for Multilingual NLP](http://www.aclweb.org/anthology/W13-3520), Rami Al-Rfou, Bryan Perozzi, and Steven Skiena. In Proceedings Seventeenth Conference on Computational Natural Language Learning (CoNLL 2013).

The Polyglot project trained their models on the English Wikipedia corpus. They embedded a vocabulary set of 100,000 words into 64 dimensions. 

We cross-referenced our set of dictionary entries with the Polyglot's vocabulary list because we only wanted to train on words that had an embedded vector representation. This resulted in a dataset of 338,637 dictionary entries for 62,663 unique words. We paritioned a third of that dataset and reserved it as a testing set.

### Recurrent Neural Networks
One of the biggest advantages of Recurrent Neural Networks (RNN) is the ability to compute mathematical operations across sequences of vectors. This fact makes them perfect for computing natural language tasks, because understanding language is sequential in nature. For humans to understand that in the sentence "In France, we spoke their native language" the word *language* refers to *French* we need to at least remember reading the word *France*. 

RNN have been able to perform even better through the development of Long Short-term Memory (LSTM) networks. On a higher level, these LSTM networks work by storing an internal cell state that 'remembers' previous information and uses that in future computation of the sequence, but the mathematical theory behind LSTM networks is beyond the scope of this write-up [^lstm].

[^lstm]: For further reading on how LSTMs work see Christopher Olah's blog on [Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/) and Andrej Kaparthy's [The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)

We used the Keras python module to implement the reverse dictionary's RNN. [Keras](http://keras.io/) is a modular, quick and easy way for implementing neural networks. It It runs on top of the [Theano](http://deeplearning.net/software/theano/) deep learning package and provides multiple outlets for customizing the network. Our implementation of the network is as follows:

- Input Layer (Input: 64 nodes)
- LSTM Layer (Output: 512 nodes)
- LSTM Layer (Output: 512 nodes)
- Fully Connected Layer with Tanh Activation (Output: 512 nodes)
- Fully Connected Layer with Linear Activation (Output: 64 nodes)

This model allowed for the network to discover any nonlinear interactions from the output of the LSTMs. Because of the limitations of the available Theano package (the HPC cluster only has Theano 0.7.0), we were not able to use Rectified Linear Units. The values of Polyglot's embeddings loosely ranged from -5 to 5. The tanh activation is limited to [-1,1] and sigmoid to [0,1], therefore we used a top layer with linear activations for the network to be able to compute the full range of embedding values.

We evaluated the network with a Euclidian Distance objective function:
$$
J(\theta) := \sqrt{(y_{pred} - y_{true})^2}
$$
Where $y_{pred}$ is the predicted dictionary entry vector and $y_{true}$ is the vector embedding of the correct dictionary entry. Keras (on top of Theano) symbolically computes the gradients of the loss function with respect to the network parameters $\theta$.

We trained the network on batch sizes of 128 training examples. Each epoch took on average 2200s using a Tesla M2090 GPU and we trained it for ### epochs. 

The final results ended in an average euclidian distance of ####.  

### User Interface

## Results
### Future Steps & Limitations
## User Guide
## Installation Guide