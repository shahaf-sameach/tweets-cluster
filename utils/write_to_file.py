from os import listdir
from os.path import isfile, join
from time import time
import threading, Queue
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

def worker(pool, result):
  while True:
    item = pool.get()
    read_file(item, result)
    pool.task_done()


def read_file(file_name, q):
  logging.debug("working on %s" %file_name)
  
  with open(file_name, 'r') as f:
    for line in f:
      try :
        tweet_id = line.split(" ")[5].split('\t')[1]
        q.put(tweet_id)
      except Exception as e:
        logging.error("Error {} in line : {}".format(e, line)) 
  
  return


if __name__ == '__main__':
  num_worker_threads = 2
  mypath = "tweets/"

  onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

  tweets_ids = []

  t0 = time()

  q = Queue.Queue()
  res_q = Queue.Queue()
  for i in range(num_worker_threads):
    t = threading.Thread(target=worker, args=(q, res_q))
    t.setDaemon(True)
    t.start()

  for file_name in onlyfiles:
    q.put("tweets/" + file_name)

  q.join()       
  t1 = time()
  print res_q.qsize()

  print "took %s sec" %(t1 -t0)

  with open('tweets_ids.txt', 'a') as f:
    while not res_q.empty():
      f.write(res_q.get() + '\n')
