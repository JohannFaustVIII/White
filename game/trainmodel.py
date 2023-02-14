import sys
import numpy as np
import tensorflow as tf
import sklearn.model_selection

def load_model(file: str):
  new_model = tf.keras.models.load_model(file)
  new_model.summary()
  return new_model

def save_model(model, file: str):
  model.save(file)

def load_data(file: str):
  x = np.loadtxt(file+'x', delimiter=",")
  y = np.loadtxt(file+'y', delimiter=",")

  x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.25)

  x_train = tf.convert_to_tensor(x_train)
  x_test = tf.convert_to_tensor(x_test)
  y_train = tf.convert_to_tensor(y_train)
  y_test = tf.convert_to_tensor(y_test)

  return x_train, y_train, x_test, y_test
  
args = sys.argv[1:]
model_file = args[0]
data = args[1]

model = load_model(model_file)
X_train, y_train, X_valid, y_valid = load_data(data)

model.fit(X_train, y_train, batch_size = 128, epochs = 20, verbose = 1, validation_data=(X_valid, y_valid))

save_model(model, model_file)