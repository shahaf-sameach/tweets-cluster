from datetime import date
import inspect

data_dict = {'var1': 'Data1', 'var2': 'Data2'}


class MyAwesomeClass:

  def __init__(self, data_dict):
    for key, value in data_dict.iteritems():
      setattr(self, key, value)


if __name__ == '__main__':
  a = MyAwesomeClass(data_dict)
  print a.var1


