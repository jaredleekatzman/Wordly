from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.callbacks import ModelCheckpoint
from keras.datasets.data_utils import get_file
from sklearn.cross_validation import train_test_split
from datetime import datetime
import numpy as np
import random
import sys
import cPickle, pickle
import theano
import theano.tensor as T
import os

SCRATCH_DIR = '/gpfs/home/fas/slade/jlk86/scratch/'
print('Loading Data...')
with open(SCRATCH_DIR + 'train_dataset.pkl') as fp:
    (X, y) = cPickle.load(fp)
n, maxlen, embedsize = X.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print('Number of Training Examples:',len(y_train))
print('Number of Testing Examples:',len(y_test))

batch_size = 128
num_epochs = 100



print('Build model...')
model = Sequential()
model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, embedsize)))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(embedsize))
model.add(Activation('relu', init = 'glorot_normal'))
model.add(Dense(embedsize))
model.add(Activation('linear', init = 'glorot_normal'))

def euclidian_dist(y_true,y_pred):
    return T.sqrt(T.sum((y_true - y_pred) ** 2, axis = 1))

home_dir = os.getenv('HOME', '/home/fas/slade/jlk86')
path = home_dir + "/weights" + datetime.now().strftime("%M%d") + ".hdf5"
checkpointer = ModelCheckpoint(filepath= path, 
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

