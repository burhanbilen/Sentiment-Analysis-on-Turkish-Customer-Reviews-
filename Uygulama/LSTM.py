from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence

class Model:
    def Analiz(veri):
        model = load_model('model.04-0.31.h5')
        
        num_words = 1000
        tok = Tokenizer(num_words=num_words)
        tok.fit_on_texts(veri)
        sequences = tok.texts_to_sequences(veri)
        yorumlar_X = sequence.pad_sequences(sequences, padding = "pre", truncating ="pre",maxlen=293)
        
        predx = model.predict(yorumlar_X)
        y_pred = [1 if i > 0.5 else 0 for i in predx]

        olumlu = (int(y_pred.count(1))/len(y_pred))*100
        
        return olumlu