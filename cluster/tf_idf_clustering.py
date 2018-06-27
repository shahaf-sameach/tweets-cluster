import string
import collections
import random
 
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_samples, silhouette_score

from utils.stuff import get_from_binary_file
from utils.nlp import process_text
 
class TfIdfCluster(object):

  def __init__(self, text):
    self.text = text
 
  def build_model(self):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)

    self.tfidf_model = vectorizer.fit_transform(self.text)
     
 
  def cluster(self, clusters=3):
    self.build_model()

    km_model = KMeans(n_clusters=clusters)
    km_model.fit(self.tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
      clustering[label].append(idx)

    silhouette_avg = silhouette_score(self.tfidf_model, km_model.labels_)
 
    return (clustering, silhouette_avg)
 
 
if __name__ == "__main__":
  sentences = ["I like that bachelor.", "I like that unmarried man.", 
               "John is very nice.", "Is John very nice?", 
               "Red alcoholic drink.", "A bottle of wine.",
               "Red alcoholic drink.", "Fresh orange juice.",
               "Red alcoholic drink.", "An English dictionary.",
               "Red alcoholic drink.", "Fresh apple juice.",
               "A glass of cider.", "A full cup of apple juice.",
               "It is a dog.", "That must be your dog.",
               "It is a dog.", "It is a log.",
               "It is a dog.", "It is a pig.",
               "Dogs are animals.", "They are common pets.",
               "Canis familiaris are animals.", "Dogs are common pets.",
               "I have a pen.", "Where do you live?",
               "I have a pen.", "Where is ink?",
               "I have a hammer.", "Take some nails.",
               "I have a hammer.", "Take some apples."]

  sentences = [t['text'] for t in get_from_binary_file()]
  random.shuffle(sentences)

  c = TfIdfCluster(sentences)
  silhouette_avgs = []
  for i in range(2, len(sentences) / 2):
    print "{}/{}".format(i, len(sentences) / 2)
    _, silhouette_avg = c.cluster(i)
    silhouette_avgs.append((i,silhouette_avg))

  m = max(silhouette_avgs, key=lambda x:x[1])
  print m

  clusters, silhouette_avg = c.cluster(m[0])

  for key, value in clusters.iteritems():
    print "cluster {}:".format(key)
    for num in value:
      print "\t{}".format(sentences[num].encode('ascii', 'ignore').strip())
    print ""

  print "The average silhouette_score is : {}".format(silhouette_avg)
