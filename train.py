from sklearn.model_selection import train_test_split
import json

with open('records2.json') as file:
    sessions = json.load(file)

with open('buys2.json') as file:
    buys = json.load(file)

import pandas as pd

features = pd.DataFrame(sessions)
labels = pd.DataFrame(buys)

# split to train and test
RANDOM_STATE = 76
TEST_SIZE = 0.2

X_train, X_test, y_train, y_test = train_test_split(features, labels,
                                                    test_size=TEST_SIZE,
                                                    shuffle=False,
                                                    random_state=RANDOM_STATE)
# end test_train_split

# FIT TRANSFORM
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

model_units = 64
dense_units = 1

from tensorflow import keras
from tensorflow.keras import layers

X_train = [X_train]
y_train = [y_train]

model = keras.Sequential()
#model.add(layers.LSTM(model_units, input_shape=shape))
model.add(layers.Dense(64, activation='sigmoid', input_shape=(1, 28)))
model.compile(loss='mean_squared_error', optimizer='adam')
model.summary()

model.fit(X_train, y_train, batch_size=100, epochs=1, verbose=2)
y = model.predict([X_test[0]])
print(y)

# {
#       "time": 0.0,
#       "user_city": "Police",
#       "product_price": 64.8,
#       "product_category": "Sprz\u0119t RTV;Przeno\u015bne audio i video;Odtwarzacze mp3 i mp4",
#       "bought": false,
#       "discount": 0
# }
