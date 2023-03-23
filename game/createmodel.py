import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.initializers import Zeros
import sys

map_size = 840

model = Sequential()
arguments = sys.argv[1:]
name = arguments[-1]
layers = arguments[:-1]
is_first = True

for layer in layers:
  if layer[0] == 'd':
    layer = layer[1:]
    model.add(Dropout(float(layer)))
  else:
    if is_first:
      model.add(Dense(int(layer), activation='relu', input_dim=map_size, kernel_initializer = 'glorot_uniform', bias_initializer = Zeros()))
      is_first = False
    else:
      model.add(Dense(int(layer), activation='relu', kernel_initializer = 'glorot_uniform', bias_initializer = Zeros()))
    model.add(BatchNormalization())

model.add(Dense(1, activation='tanh'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.save(name)