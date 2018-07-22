import string

from nltk import word_tokenize, PorterStemmer


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    try:
        text = text.encode('ascii', 'ignore')
        text = text.translate(None, string.punctuation)
    except Exception as e:
        print text
        raise e
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens