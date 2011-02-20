import time, math
from random import Random

RANDOM = Random() # Shared random instance to ensure deterministic behaviour
                  # for replays. DO NOT use this instance in an agent.

class Timer:
    def __init__(self, string=None):
        self.string = string
        self.t = None
    
    def elapsed(self):
        return time.clock() - self.t
        
    def __enter__(self):
        self.t = time.clock()
        return self
        
    def __exit__(self, type, value, traceback):
        if self.string:
            print self.string % (round(self.elapsed(), 4),)