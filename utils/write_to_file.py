import os
from time import time
import threading, Queue
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')


dir = os.path.dirname(__file__)
dir_path = os.path.join(dir, '../files/tweets/')

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

  onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

  tweets_ids = []

  t0 = time()

  q = Queue.Queue()
  res_q = Queue.Queue()
  for i in range(num_worker_threads):
    t = threading.Thread(target=worker, args=(q, res_q))
    t.setDaemon(True)
    t.start()

  for file_name in onlyfiles:
    if len(file_name) > 5:
      q.put(dir_path + file_name)

  q.join()       
  t1 = time()
  print res_q.qsize()

  print "took %s sec" %(t1 -t0)

  with open(dir_path + 'tweets_ids.txt', 'a') as f:
    while not res_q.empty():
      f.write(res_q.get() + '\n')
