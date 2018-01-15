from gensim.models import Word2Vec
from nltk.corpus import brown
# import nltk

# nltk.download('brown')
b = Word2Vec.load('word2vec_model')
# b = Word2Vec(brown.sents())
# b.save('word2vec_model')
print b.most_similar('money', topn=5)