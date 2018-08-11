from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.text_proccesing import process_text


class TfIdfModel(object):

    def __init__(self):
        pass

    def build(self, tweets):
        """ Transform texts to Tf-Idf coordinates """
        text = [t['text'] for t in tweets]
        vectorizer = TfidfVectorizer(tokenizer=process_text,
                                     stop_words=stopwords.words('english'),
                                     max_df=0.5,
                                     min_df=0.1,
                                     lowercase=True,
                                     max_features=10000)

        return vectorizer.fit_transform(text)



# TfIdfModel().build(tweets)

