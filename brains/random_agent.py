import random
import math
from pprint import pprint
from math import pi

class AgentBrain():
    def __init__(self):
        """Put any initialization code here."""
        pass
    
    
    def action(self, observation):
        #pprint(observation)
        action = {
            'turn': random.random()*pi/1.5 - pi/3,
            'speed': random.random()*50,
            'shoot': random.random() > 0.9 #shoot 10% of the turns
        }
        return action