from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.callbacks import ModelCheckpoint
from keras.datasets.data_utils import get_file
from sklearn.cross_validation import train_test_split
import numpy as np
import random
import sys
import cPickle, pickle
import theano
import theano.tensor as T
import os
import h5py
from datetime import datetime

def configure_arguments(parser):
    parser.add_argument('-d','--dataset')
    parser.add_argument('-s','--save_file')
    parser.add_argument('-e','--num_epochs',type=int,default=25)

def train_rnn(num_epochs = 25, dataset= '/home/fas/slade/jlk86/scratch/train_dataset.pkl', 
    save_path = '/home/fas/slade/jlk86/weights.h5'):

    print('Loading Data...')
    if dataset.endswith('.pkl'):
        with open(dataset) as fp:
            (X, y) = cPickle.load(fp)
    elif dataset.endswith('.h5'):
        h5f = h5py.File(dataset,'r')
        X = h5f['X']
        y = h5f['y']
        h5f.close()

    n, maxlen, embedsize = X.shape

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    print('Number of Training Examples:',len(y_train))
    print('Number of Testing Examples:',len(y_test))

    batch_size = 128
    num_epochs = num_epochs

    print('Build model...')
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, embedsize)))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(embedsize, init='glorot_normal'))
    model.add(Activation('linear'))

    def euclidian_dist(y_true,y_pred):
        return T.sqrt(T.sum((y_true - y_pred) ** 2, axis = 1))

    checkpointer = ModelCheckpoint(filepath= save_path, 
                                   verbose=1, save_best_only=True)

    print('Train...')
    model.compile(loss=euclidian_dist, optimizer='rmsprop')
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=num_epochs,
             validation_data=(X_test,y_test), show_accuracy = True,
             callbacks=[checkpointer])
    score, acc = model.evaluate(X_test, y_test,
                               batch_size = batch_size,
                               show_accuracy = True)
    print('Test score:', score)
    print('Test accuracy:', acc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    print args

    train_rnn(args.num_epochs, args.dataset, args.save_file)

