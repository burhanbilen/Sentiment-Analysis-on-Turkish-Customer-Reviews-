# Sentiment Analysis on Turkish Customer Reviews

This project is based on various customer reviews from different stores and the model uses LSTM Network.

1) From Zemberek NLP library for Turkish language, spell checking and noise normalization classes were used along with regular expression operations to prepare the data for the training phase. The destination of the text preprocessing codes is the "Normalizasyon ve Yazım Denetimi" folder.

2) The preprocessed dataset and raw codes of the deep learning model are in the "Model Eğitim ve Test Aşaması" folder. In this phase, neural network model was saved as .h5 file(MODEL.h5), to use it each time without training again.

3) Finally, main application destination is the "Uygulama" folder. Here, you should run the "Arayüz.py" first to be able to run all codes properly.


*Arayüz.py: User Interface

*eMagaza.py: Scraping Amazon Customer Reviews
*LSTM.py: Use of the Saved Model and Finding the Positive Reviews
