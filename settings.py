import logging

users = [
{'access_key' : "893338040-Xwr6feArQMSw4aZFtelB1uJltJu8KO7ntVuJjxGA",
 'access_secret' : "uZiNMkZVjSQIAyI7eGfWIiBZavLCrxjqVBnzRm3DYIxV4",
 'consumer_key' : "q2sT4V5awnmduVmrrREtQvt9w",
 'consumer_secret' : "UqLNJzvwj6JUDpUsEnckNpyfBUK40ROPqXjw5bqLCcZClIXbpd"},

{'access_key' : "739456478789177346-aVxH9dMsFTnXjfpo009hbHOXPOPNLD2",
 'access_secret' : "oqzjbVEaYhK1t3bCL9Guxz3hb8x628rESK3PdhGgXMenQ",
 'consumer_key' : "lQdgArnZubvEMImRulCPgXc4d",
 'consumer_secret' : "Lnsu5wxYlaVg6WZvlp3AlWNrpnR7L6tSpNWfdDKtW8v7GVHyXP"},

{'access_key' : "39455973-2cRfVxauYn6o4hzEFoMBAFWf5ZD0EG9OaFLQZrma9",
 'access_secret' : "1zdfbjLypaxLQnj6YzNZsYGUzpzTLJJ2TJWqckTvQJEDO",
 'consumer_key' : "Supf7AjO1907tRzehTUjgMMqC",
 'consumer_secret' : "yr9aZHs4z1wfRAlQbxr8JtcbUGYqj7RM6nCMUHH1eLiMlyoCAu"},

{'access_key' : "35890867-qB442BKbTc3xuENaBuYdMzq3xa3XzzvApmDW8HMOA",
 'access_secret' : "Eg487GZRP6GsxAIIfViO14V9MgPnEtv5Sh6xDBFtx0",
 'consumer_key' : "IK7lcKA63xgcyTab2Xp2DA",
 'consumer_secret' : "VCzmsjfZOyJQsixP9vVp8Ur2AiKkm4tinJmfHUK4"}]

class User:
  def __init__(self, data_dict):
    for key, value in data_dict.iteritems():
      setattr(self, key, value)

class TwitterSettings:
  all_users = [User(user) for user in users]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)[%(funcName)]-20s) %(message)s')


try :
  from local_settings import *
except ImportError:
  pass




