# Import libraries

import tensorflow as tf
import pandas as pd

#%% Load Model

model = tf.keras.models.load_model('my_model.h5')

#%% Pull in raw data for sample prediction

data = pd.read_csv('fbdh1.csv')

