import math, random, time
from math import pi

class AgentBrain():
    """ This agent is a bit slow and takes 0.1 second for each turn. """
    def __init__(self):
        """ Put any initialization code here. It is not limited in execution
        time."""
        pass
    
    def action(self, observation):
        time.sleep(0.1)
        action = {
            'turn': random.random()*pi/1.5 - pi/3,
            'speed': 50,
            'shoot': random.random() > 0.9
        }
        
        return action