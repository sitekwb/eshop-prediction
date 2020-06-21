from sklearn.model_selection import train_test_split
import json

with open('records2.json') as file:
    sessions = json.load(file)

buys = []

for session in sessions:
    buys.append([])
    buys_in_session = buys[-1]
    for i in range(len(session)):
        event = session[i]
        buys_in_session.append(event['bought'])
        del event['bought']
        session[i] = list(event.values())

# import pandas as pd
#
# labels = pd.DataFrame(buys)
# features = pd.DataFrame(sessions)

labels = buys
features = sessions

# split to train and test
RANDOM_STATE = 76
TEST_SIZE = 0.2

X_train, X_test, y_train, y_test = train_test_split(features, labels,
                                                    test_size=TEST_SIZE,
                                                    shuffle=False,
                                                    random_state=RANDOM_STATE)
# end test_train_split

# TODO FIT TRANSFORM

# TODO delete
# max_session_len = 0
#
# for session in features:
#     max_session_len = max(max_session_len, len(session))
#
# print(max_session_len)  # -> 11

model_units = 64

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np

shape = pd.DataFrame(X_train).shape
print(shape)

model = keras.Sequential()
model.add(layers.LSTM(model_units, input_shape=shape))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam')
model.summary()

a = tf.convert_to_tensor(X_train)
type(X_train)

# model.fit(a, y_train, epochs=1, batch_size=100, verbose=2)

# {
#       "time": 0.0,
#       "user_city": "Police",
#       "product_price": 64.8,
#       "product_category": "Sprz\u0119t RTV;Przeno\u015bne audio i video;Odtwarzacze mp3 i mp4",
#       "bought": false,
#       "discount": 0
# }
