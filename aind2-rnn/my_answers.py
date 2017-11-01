import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras
import string


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []
    start = 0
    end = start + window_size
    while end < len(series):
        X.append(series[start:end])
        start += 1
        end += 1
    y = series[window_size:]
    # reshape each 
    X = np.asarray(X)
    y = np.asarray(y)
    y = np.reshape(y, (len(y),1))
    
    assert(type(X).__name__ == 'ndarray')
    assert(type(y).__name__ == 'ndarray')
    assert(X.shape == (len(series) - window_size, window_size))
    assert(y.shape in [(len(series) - window_size,1), (len(series) - window_size,)])
    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape = (window_size,1)))
    model.add(Dense(1))
    return model

### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    allowed_chars = set(punctuation + list(string.ascii_lowercase) + [' '])
    chars = set(text)
    unwanted_characters = chars - allowed_chars
    for mark in unwanted_characters:
        text = text.replace(mark,' ')
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    start = 0
    while start + window_size < len(text):
        end = start + window_size
        inputs.append(text[start:end])
        outputs.append(text[end])
        start += step_size
        
    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape = (window_size,num_chars)))
    model.add(Dense(num_chars, activation = 'softmax'))
    #model.add(Activation('softmax'))
    return model
