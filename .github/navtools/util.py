from time import time

# A simple precision timer wrapper with a context
class Timer(object):
  def __init__(self, context):
    self.context = context

  def __enter__(self):
    self.start = time()
  
  def __exit__(self, exc_type, exc_value, traceback):
    passed = time() - self.start
    if passed > 0.001:
      print(f'"{self.context}" took {passed:.3f} sec')
  