import logging


class TwitterSettings:
  pass

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-10s) [%(funcName)-10s] %(message)s')


try :
  from local_settings import *
except ImportError:
  pass




