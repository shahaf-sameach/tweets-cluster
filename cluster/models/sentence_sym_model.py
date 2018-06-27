import numpy as np
from time import time

from utils.sentence_sym import sentence_distance
from utils.stuff import get_from_binary_file



class SentenceSymModel(object):

    def __init__(self):
        pass

    def build(self, sentences):
        m = np.zeros((len(sentences), len(sentences)))
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                if i == j:
                    m[i][j] = 1.0
                else:
                    sim = sentence_distance(sentences[i], sentences[j])
                    m[i][j] = sim
                    m[j][i] = sim
        return m


if __name__ == "__main__":
    t0 = time()

    sentences = [t['text'] for t in get_from_binary_file()[:30]]
    t1 = time()
    print  "loading took {}".format(t1 - t0)
    model = SentenceSymModel()
    dist_matrix = model.build(sentences)
    print dist_matrix
    t2 = time()
    print "calc matrix took {}".format(t2 - t1)