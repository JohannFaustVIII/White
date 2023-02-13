# just an example, to be used later

import sys
import tensorflow as tf

name = sys.argv[1]

new_model = tf.keras.models.load_model(name)

new_model.summary()