import pygame, math, utils
from pygame.locals import *
from ammo_pack import AmmoPack
from agent_proxy import AgentProxy
from control_point import ControlPoint
from game_object import Wall
from team import BlueTeam, RedTeam
from settings import *

class World:
    """ Keeps track of the current state of the world. """
    def __init__(self, red_brain, blue_brain, level):
        self.level = __import__(level)
        
        #the surface that all objects will be drawn on
        self.game_surface = pygame.Surface(self.level.WORLD_SIZE)
        #used for keeping all agents in bounds
        self.rect = pygame.Rect(((0,0), self.level.WORLD_SIZE))
        #font for score
        self.font = pygame.font.SysFont("Arial Black,Tahoma,Comic Sans MS",20)
        #surface to draw score on
        self.score = pygame.Surface((0,0))
        #updating is true of a 
        # groups per object
        self.control_points = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.ammo_packs = pygame.sprite.Group()
        #the container for all game objects, except agents.
        self.static_objects = pygame.sprite.LayeredUpdates()
        #the container for observer sprites
        self.observers = pygame.sprite.Group()
        self.draw_observers = False
        #container for shot sprites
        self.shots = pygame.sprite.Group()
        
        #spawn control points
        for location in self.level.CONTROL_POINTS:
            self.control_points.add(ControlPoint(self, location))
        self.static_objects.add(self.control_points)

        #spawn walls
        for (position, size) in self.level.WALLS:
            self.walls.add(Wall(position, size))
        self.static_objects.add(self.walls)

        #spawn teams
        self.teams = (BlueTeam(self, blue_brain), RedTeam(self, red_brain))
        for team in self.teams:
            for _ in xrange(self.level.PLAYERS_PER_TEAM):
                team.spawn_agent(self)
                
        #spawn ammo packs
        for _ in range(self.level.DEFAULT_AMMO_PACKS):
            self.ammo_packs.add(AmmoPack(self))
        self.static_objects.add(self.ammo_packs)

    def render(self, viewport):
        #set the background to green
        self.game_surface.fill((93, 255, 79))
        
        #draw all game objects when they're within the viewport
        self.static_objects.draw(self.game_surface)
        for team in self.teams:
            team.draw(self.game_surface)
            
        if self.draw_observers:
            self.observers.draw(self.game_surface)
            
        self.shots.draw(self.game_surface)

        viewport.render(self.game_surface, self.score)

    def simulation_step(self):
        for team in self.teams:
            team.update()
        self.static_objects.update()
        self.shots.update()
    
    def action_step(self):
        """ Ask all agents what their new action is """
        if utils.RANDOM.random() < self.level.AMMO_SPAWN_PROB:
            new_ammo = AmmoPack(self)
            self.ammo_packs.add(new_ammo)
            self.static_objects.add(new_ammo)

        for cp in self.control_points:
            cp.get_team().update_score(1)
            
        try:
            scoreString = ""
            for team in self.teams:
                scoreString += str(team) + "    "
            self.score = self.font.render(scoreString, False, pygame.Color('White'))
        except:
            #Sometimes, font.render() throws an error that the width is 0.
            #this CAN NOT be true, but this error somehow occurs...
            pass
        
        #update the observers first, so they get drawn properly.
        for observer in self.observers:
            observer.update()
            
        self.draw_observers = True
        for team in self.teams:
            with utils.Timer() as t:
                team.action()
                team.stats["time"] += t.elapsed()
        self.draw_observers = False
    
    def touching_objects(self, object):
        """ Returns a list of GameObjects that touch with object """
        return [o
                for group in (self.static_objects,) + self.teams
                for o in  pygame.sprite.spritecollide(object, group,
                    dokill = False, collided = pygame.sprite.collide_mask)
                if o != object]
        
    def is_touching(self, object):
        """ Returns true if this object touches another object """
        return len(self.touching_objects(object)) > 0
        
    def colliding_objects(self, object):
        """ Returns a list of GameObjects this object is colliding with.
        A collision can only take place with an object that has its collide
        member set to True. """
        return [o for o in self.touching_objects(object) if o.collide]
    
    def is_colliding(self, object):
        """ Returns true if the object collides with any collidable game object """
        # Okke, pygame.sprite.spritecollideany seems more efficient.
        # Arjan, this is true. However, it does not check wether an object is
        #   collidable or not. ("if o.collide" part)
        return len(self.colliding_objects(object)) > 0

    def visible_objects(self, obj, group):
        """ Match object visibility (enlarged mask) with a given group. """
        visibles = [o
                    for o in pygame.sprite.spritecollide(obj, group,
                      dokill = False, collided = pygame.sprite.collide_mask)
                    if o != obj]
        return visibles
    
    def cleanup(self):
        for team in self.teams:
            print team.name, team.score, team.stats
