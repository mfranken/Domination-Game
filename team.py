import pygame, time, collections, traceback
from pygame.sprite import LayeredDirty
from agent_proxy import AgentProxy
from settings import *

class Team(LayeredDirty):
    players = 0
    dirty = 2 #always redraw
    def __init__(self, world):
        LayeredDirty.__init__(self)
        
        self.world = world
        self.name = None #the name of the team
        self.suit = None #the pygame.image that shows the team
        self.controlpoint = None #the pygame.image of an controlpoint when this team controls it
        self.brain = None #the AgentBrain class that all agents of this team use to generate actions
        self.spawn_point = (0,0) #the spawning location of this team in the current map
        self.score = 0 #the score of the team in this game
        
        self.stats = collections.defaultdict(float) #saves all the statistics.
    
    def update_score(self, points):
        self.score += points
        
    def spawn_agent(self, world):
        #this is a bit of a hack. It accesses the class variable player that belongs to
        #BlueTeam or RedTeam.
        type(self).players += 1
        self.add(AgentProxy(type(self).players, world, self), layer=4)
    
    def action(self):
        # If at some point the agents before the current took to long
        # to react (cumulative), every next agent becomes .noop().
        observations = {}
        for agent in self.get_sprites_from_layer(4):
            observations[agent] = agent.observe()
        
        max_t = time.clock() + self.world.level.RESPONSE_TIME
        for agent, observation in observations.iteritems():
            if time.clock() < max_t:
                try:
                    agent.action(observation)
                except Exception as ex:
                    print ex
                    traceback.print_exc(file=sys.stdout)
                    self.stats["exceptions"] += 1
            else:
                print 'Agent took too long. %.3f > %.3f' %(time.clock(), max_t) #[EDITED]
                agent.noop()
                
    #All these getters and setters aren't really pythonic.
    def get_suit_image(self):
        return self.suit
    
    def get_spawn_point(self):
        return self.spawn_point
    
    def get_controlpoint_image(self):
        return self.controlpoint
    
    def get_brain(self):
        return self.brain()
    
    def __str__(self):
        return "%s: %s" % (self.name, self.score)
        
class BlueTeam(Team):
    def __init__(self, world, brain):
        Team.__init__(self, world)
        self.name = "Blue"
        self.suit = pygame.image.load('graphics/blue_agent.png').convert_alpha()
        self.controlpoint = pygame.image.load('graphics/blue_control.png').convert_alpha()
        self.spawn_point = self.world.level.BLUE_SPAWN_POINT
        try:
            brain_package = __import__(brain)
            self.brain = brain_package.AgentBrain
        except ImportError as e:
            print "The blue agent brain could not be loaded. Does the file %s exist?" % (brain)
            raise
        
class RedTeam(Team):
    def __init__(self, world, brain):
        Team.__init__(self, world)
        self.name = "Red"
        self.suit = pygame.image.load('graphics/red_agent.png').convert_alpha()
        self.controlpoint = pygame.image.load('graphics/red_control.png').convert_alpha()
        self.spawn_point = self.world.level.RED_SPAWN_POINT
        try:
            print brain
            brain_package = __import__(brain)
            self.brain = brain_package.AgentBrain
        except ImportError as e:
            print "The red agent brain could not be loaded. Does the file %s exist?" % (brain)
            raise
        
        
class NeutralTeam(Team):
    """ This team provides easy access to neutral team colors for ControlPoints. """
    def __init__(self):
        Team.__init__(self, None)
        self.name = "Neutral"
        self.controlpoint = pygame.image.load('graphics/neutral_control.png').convert_alpha()
    
    def spawn_player(self):
        raise NotImplementedError("Neutral player can not spawn agents")
