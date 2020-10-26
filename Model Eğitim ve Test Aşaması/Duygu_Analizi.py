import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.layers.embeddings import Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import confusion_matrix

df = pd.read_csv("magaza_yorumlari_oo.csv", encoding = "utf-16")

gorusler = df['Görüş']

df["Durum"].replace({"Olumlu": 1, "Olumsuz": 0}, inplace=True)
durumlar = df['Durum']

veri = list(zip(gorusler, durumlar))

X = []
y = []
for v in veri:
    X.append(v[0])
    y.append(v[1])

X = np.array(X)
y = np.array(y).reshape(-1,1)

num_words = 5000
tok = Tokenizer(num_words=num_words)
tok.fit_on_texts(X)
sequences = tok.texts_to_sequences(X)
X_new = sequence.pad_sequences(sequences, padding = "pre", truncating ="pre")

X_train,X_test,y_train,y_test = train_test_split(X_new, y, test_size=0.10, random_state=42)

model = Sequential()
model.add(Embedding(num_words, 172, input_length=X_train.shape[1]))
model.add(LSTM(188, recurrent_dropout = 0.3, dropout = 0.5))
model.add(Dense(1, activation = "sigmoid"))

model.summary()

model.compile(loss='binary_crossentropy',optimizer='rmsprop', metrics=['accuracy'])

my_callbacks = [
    EarlyStopping(patience=3),
    ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5')
]
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split = 0.15, callbacks = my_callbacks)

loss,accuracy = model.evaluate(X_test, y_test)
print("loss: ", loss)
print("accuracy: ", accuracy)

predx = model.predict(X_test)
y_pred = np.array([1 if i > 0.5 else 0 for i in predx]).reshape(-1,1)
print(confusion_matrix(y_test, y_pred))

y_pred_new = [i for i in y_pred]
olumlu = (int(y_pred_new.count(1))/len(y_pred_new))*100
