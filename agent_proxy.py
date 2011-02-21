from __future__ import division
from game_object import GameObject
import copy, math, pygame, utils, replay
from pygame.locals import *
import pygame
from settings import *

# global constants for sound
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished
SOUND = False  # enable sound after initialisation

try:
    pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    laser = pygame.mixer.Sound('sounds/laser.wav' )
    monsterkill = pygame.mixer.Sound('sounds/monsterkill.wav' )
    doublekill = pygame.mixer.Sound('sounds/doublekill.wav' )
    godlike = pygame.mixer.Sound('sounds/godlike.wav' )
    SOUND = True
except pygame.error, exc:
    print >>sys.stderr, "Could not initialize sound system: %s" % exc


class AgentProxy(GameObject):
    """ Any agent that can move through the environment. """
    kills = 0
    
    def __init__(self, number, world, team):
        GameObject.__init__(self)
        self.collide = True
        self.dirty = 2 #always redraw
        
        self.number = number
        self.world = world
        self.team = team

        self.base_image = self.team.get_suit_image()
        self.rect = self.base_image.get_rect()
        self.mask = pygame.mask.from_surface(self.base_image)
        self.image = self.base_image
        self.font = pygame.font.SysFont("Arial", 9)
        
        self.observer = ObservationSprite(world, self, SIGHT)
        self.brain = self.team.get_brain()
        
        self.label = ''

        self.alive = False
        self.spawn()        
    
    def spawn(self):
        """ set initial state of this agent """
        self.direction = utils.RANDOM.random()*math.pi*2 - math.pi
        self.redraw_image()
        self.speed = 0
        self.ammo = self.world.level.DEFAULT_AMMO
        self.alive = True
        self.kills = 0
        
        # Find a spawn point.
        # This loop might in theory take forever to return. In practice,
        # it returns within a reasonable number of iterations

        self.rect.center = self.team.get_spawn_point()
        while self.world.is_colliding(self):
            self.rect.centerx += utils.RANDOM.choice((-10, 10))
            self.rect.centery += utils.RANDOM.choice((-10, 10))
            self.rect.clamp_ip(self.world.rect) #never search outside the world
            
        #location keeps a floating point representation of the center of the
        #agent, mirroring the self.rect.center with higher precision.
        self.location = self.rect.center

        self.team.stats["spawns"] += 1
    
    def noop(self):
        self.speed = 0
        
    def observe(self):
        return self.observer.observe()
        
    def action(self, observation = None):
        """ Ask the brain what move to make. Turn and shoot immediately. """
        if observation == None:
            observation = self.observer.observe()
        
        action = self.brain.action(observation)
        replay.record(self.number, self.team.name, action)
    
        if 'speed' in action:
            speed = action['speed']
            #ensure bounds
            speed = max(speed, MIN_SPEED)
            speed = min(speed, MAX_SPEED)
            self.speed = speed
        
        if 'turn' in action:
            turn = action['turn']
            turn = min(turn, MAX_TURN)
            turn = max(turn, -MAX_TURN)
            self.direction += turn
            if self.direction <= -math.pi:
                self.direction += math.pi*2
            elif self.direction > math.pi:
                self.direction -= math.pi*2
            
        if 'shoot' in action:
            self.shoot = bool(action['shoot'])
            
            if self.shoot and self.ammo > 0:
                self.ammo -= 1
                shot = ShootSprite(self.world, self)
                self.world.shots.add(shot)
                if SOUND :                    
                    laser.play()   
                killed_agents = shot.killed_agents()
                if len(killed_agents) > 1 and SOUND:
                    doublekill.play()            
                for killed_agent in killed_agents:
                    self.kills += 1
                    if self.kills == 6 and SOUND:
                        print str(self),' got a monsterkill!!!'
                        monsterkill.play()  
                    elif self.kills == 10 and SOUND:
                        print str(self),' is godlike!!!'
                        godlike.play()  
                    if PRINT_DEBUG:
#                        print str(killed_agent), "got killed by", str(self)                        
                        pass
                    killed_agent.alive = False
                    self.team.stats["kills"] += 1                    
        
        if 'label' in action:
            self.label = action['label']
        
    def update(self):
        """ move """
        if self.alive == False:
            if PRINT_DEBUG:
#                print str(self), "spawns"
                pass
            self.spawn()
            return
        
        old_rect = copy.copy(self.rect)
        direction = self.direction
            
        self.redraw_image()
        
        distance = self.speed / SIMULATION_RESOLUTION

        x = self.location[0] + distance * math.cos(direction)
        y = self.location[1] + distance * math.sin(direction)
        
        #make sure we don't run off the map. Don't use rect.clamp, as this
        #rounds the location off to an integer representation.
        x = min(max(x, self.rect.w/2), self.world.rect.w - self.rect.w/2)
        y = min(max(y, self.rect.h/2), self.world.rect.h - self.rect.h/2)

        self.location = (x, y)
        self.rect.center = self.location
        
        if self.world.is_colliding(self):
            self.rect = old_rect
            self.location = self.rect.center
            
    def redraw_image(self):
        image = self.base_image.copy()
        looking_direction = (self.rect.w/2 + math.cos(self.direction)*10,
                             self.rect.h/2 + math.sin(self.direction)*10)
        #draw looking direction
        pygame.draw.line(image, (0,0,0), (self.rect.w/2,self.rect.h/2), looking_direction, 3)
        
        #draw label
        if self.label:
            text = self.font.render(self.label, False, pygame.Color('White'))
            image.blit(text, (2, 0))
            
        self.image = image
        
    def __str__(self):
        return "%s#%s @ %s" % (self.team.name, self.number, self.rect.center)
        
class ShootSprite(pygame.sprite.DirtySprite):
    def __init__(self, world, agent):
        pygame.sprite.DirtySprite.__init__(self)
        self.world = world
        self.agent = agent
        self.max_dist = MAX_SHOT_DISTANCE
        self.direction = self.agent.direction
        
        #set up images
        self.base_image = pygame.Surface((self.max_dist*2, self.max_dist*2)).convert_alpha()
        self.base_image.fill(pygame.Color(255,255,255,0)) #transparent
        if self.agent.team.name == 'Red' :
            self.shot_color = pygame.Color(255,0,0,255) #red
        else :
            self.shot_color = pygame.Color(0,0,255,255) #Blue
        self.rect = self.base_image.get_rect()
        self.rect.center = self.agent.rect.center
        self.image = None
        self.mask = None
        self.draw_shot(self.max_dist/2, self.max_dist/4)
        
        #using the self.image and self.mask that was set by find_first_wall
        self.kills = []
        for team in self.world.teams:
            self.kills.extend( [ agent
                            for agent
                            in self.world.visible_objects(self, team)
                            if agent != self.agent] )
        
        self.time_to_live = 10
        
    def killed_agents(self):
        return self.kills
    
    def update(self):
        self.time_to_live -= 1
        if self.time_to_live < 1: self.kill()
        
        #is the next line VERY SLOW?
        self.image.fill((0,0,0,25), None, BLEND_RGBA_SUB) #slowly fade out shot
    
    def draw_shot(self, dist, stepsize):
        """ Recursive function that does a binary search in the distance, until
        the maximum shooting distance is found that does not touch a wall.
        Recurses ceil(math.log(self.max_dist)) times.
        The side effect of changing self.image and self.mask is intentional!"""
        if stepsize < 1:
            return dist
        
        self.image = self.base_image.copy()
        shoot_to = (self.rect.w/2 + math.cos(self.direction)*dist,
                    self.rect.h/2 + math.sin(self.direction)*dist)
        
        pygame.draw.line(self.image, self.shot_color, (self.rect.w/2,self.rect.h/2), shoot_to, 1)
        #the third argument is a threshold value. Apparently, it doesn't work without it.
        self.mask = pygame.mask.from_threshold(self.image, self.shot_color, (1,1,1))

        if(self.world.visible_objects(self, self.world.walls)):
            return self.draw_shot(dist-stepsize, stepsize/2)
        else:
            return self.draw_shot(dist+stepsize, stepsize/2)
        
class ObservationSprite(pygame.sprite.DirtySprite):
    def __init__(self, world, agent, sight):
        pygame.sprite.DirtySprite.__init__(self)
        
        self.world = world
        self.agent = agent
        
        self.image = pygame.Surface((sight*2, sight*2)).convert_alpha()
        self.image.fill(pygame.Color(255,255,255,0)) #transparent
        pygame.draw.circle(self.image, (255,255,255,20), (sight, sight), sight)
        pygame.draw.circle(self.image, (0,0,0,127), (sight,sight), sight, 1)
        self.collide = False
        
        self.rect = self.image.get_rect()
        self.rect.center = self.agent.rect.center
        
        self.mask = pygame.mask.from_surface(self.image, 0)
        
        self.world.observers.add(self)

    def update(self):
        self.rect.center = self.agent.rect.center
        
    def observe(self):
        """Return all observed information when observing from the position the
        agent is at. """
        self.rect.center = self.agent.rect.center
        
        # Control Points.
        # All control points are visible.
        control_points = [
            {
                'team': o.team.name,
                'location': o.rect.center
            } 
            for o in self.world.control_points
        ]

        # Walls.
        # Only walls within range within range are visible.
        # Simplification that seeing part of a wall (Rect)
        # means seeing the entire wall-part does seem reasonable.
        walls = [
            {
                'top': o.rect.top,
                'left': o.rect.left,
                'bottom': o.rect.bottom,
                'right': o.rect.right
            }
            for o in self.world.visible_objects(self, self.world.walls)
        ]
       
        # Ammo Packs.
        # Only ammo packs within range are visible.
        ammo_packs = [ {'location': o.rect.center}
            for o in self.world.visible_objects(self, self.world.ammo_packs)
        ]

        # Agents.
        # Only agents within range are visible, whether they are on your own team
        # or on the other team.
        agents = []
        for team in self.world.teams:
            agents += [
                {
                    'team': team.name,
                    'location': agent.rect.center,
                    'direction': agent.direction,
                    'id': agent.number
                }
                for agent
                in self.world.visible_objects(self, team)
                if agent != self.agent
            ]

        observation =  {
            'id': self.agent.number,
            'location': self.agent.rect.center,
            'ammo': self.agent.ammo,
            'direction': self.agent.direction,
            'team': self.agent.team.name,
            'respawn': not self.agent.alive,
            'agents': agents,
            'controlpoints': control_points,
            'walls': walls,
            'ammopacks': ammo_packs,
        }
        
        return observation
