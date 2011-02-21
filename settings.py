import math, sys

#debugging settings
PRINT_DEBUG = True
SOUND = True

#global settings, should not change between games
SIGHT = 100 #pixels of sight an agent has
MAX_SHOT_DISTANCE = 60 #distance an agent can shoot, needs to be smaller than SIGHT.
AGENT_SIZE = 5 #agent radius
GUI_SIZE = (800, 800) #size of the window in pixels
MAX_TIMESTEPS = 4000

#agent movement settings
#simulation resolution should not be set too low. MAX_SPEED / SIMULATION_RESOLUTION
#gives the accuracy of the collision detection. 50/10 means it can be 5 pixels off
SIMULATION_RESOLUTION = 10 #the number of timesteps between each AI event
MAX_SPEED = 40 #the maximum speed of an agent (pixels between each AI event)
MIN_SPEED = 0 #the minimum speed of an agent
MAX_TURN = math.pi/3 #the maximum turning angle of an agent in radians

sys.path.append("brains") #add brains dir to path to easily import them
sys.path.append("levels") #add levels dir to path to easily import them
#settings that should be set by the command line
RED_BRAIN = "claiming_agent"
BLUE_BRAIN = "claiming_agent"

