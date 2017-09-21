import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras
import re
import string

# TODO: fill out the function below that transforms the input series
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    length = np.size(series) # obtain the length of the series
    X = [ series[i: i+window_size] for i in range(length-window_size) ]
    y =[ series[i+window_size] for i in range(length-window_size) ]

    # reshape each
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    # build model using keras documentation recommended optimizer initialization
    optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    # compile the model
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    ASCII_LETTERS = string.ascii_lowercase
    ENGLISH_PUNCTUATION = ',.!?;:'

    # find all unique characters in the text
    uniques = ''.join(set(text))

    # remove as many non-english characters and character sequences as you can
    if uniques is not None:
        for char in uniques:
            if char not in ASCII_LETTERS and char not in ENGLISH_PUNCTUATION:
                text = text.replace(char, ' ')

        # shorten any extra dead space created above
        text = text.replace('  ',' ')

    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    length = len(text) # obtain the length of the series
    inputs = [ text[i: i+window_size] for i in range(0, length - window_size, step_size) ]
    outputs =[ text[i+window_size] for i in range(0, length - window_size, step_size) ]

    return inputs,outputs

# TODO build the required RNN model:
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars, activation='softmax'))
    # initialize optimizer
    optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    # compile model --> make sure initialized optimizer and callbacks - as defined above - are used
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model
