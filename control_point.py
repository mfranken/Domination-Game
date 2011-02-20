from game_object import GameObject
from team import NeutralTeam, BlueTeam, RedTeam
import pygame
from settings import *

class ControlPoint(GameObject):
    """ A control point belongs to the team of the agent that stands on top of it.
    """
    
    def __init__(self, world, position):
        GameObject.__init__(self)
        self.world = world

        self.alignment = 0
        self.neutralteam = NeutralTeam()
        self.team = self.neutralteam
        self.image = self.team.get_controlpoint_image()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.layer = 1
            
    def update(self):
        owners = self.world.colliding_objects(self)
        
        #if all agents on the control point are of the same team
        if len(set([o.team for o in owners])) == 1 and owners[0].team != self.team:
            self.team = owners[0].team
            self.image = self.team.get_controlpoint_image()
            self.dirty = 1
            
    def get_team(self):
        return self.team