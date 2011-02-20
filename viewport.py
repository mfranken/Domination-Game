import pygame
from pygame.locals import *
from settings import *

class Viewport:
    def __init__(self):
        self.world_rect = pygame.Rect((0,0), (0,0))
        self.rect = pygame.Rect((0,0), (0,0))
        self.screen = pygame.display.set_mode(GUI_SIZE, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.rect.size = self.screen.get_size()
        
    def set_world(self, world):
        """ world_rect needs to be set before resize or move_offset are called.
        We can't do this in the init(), as the world does not exist before
        the viewport is created. This can not be turned around, as the images
        are loaded during the creation of the world, and they need a display
        mode to have been set. """        
        self.world_rect = world.rect
        
    def resize(self, size):
        pygame.display.set_mode(size, RESIZABLE | HWSURFACE | DOUBLEBUF)
        self.rect = pygame.Rect(self.rect.topleft, self.screen.get_size())
        
        if not self.world_rect.collidepoint(self.rect.center):
            self.rect.centerx = max(self.world_rect.left, self.rect.centerx)
            self.rect.centerx = min(self.world_rect.right, self.rect.centerx)
            self.rect.centery = max(self.world_rect.top, self.rect.centerx)
            self.rect.centery = min(self.world_rect.bottom, self.rect.centerx)
            
        
    def render(self, surface, overlay):
        self.screen.fill((0,0,0))
        self.screen.blit(surface, (-self.rect.left, -self.rect.top))
        self.screen.blit(overlay, (10, 5))
    
    def move_offset(self, offset):
        oldrect = self.rect.copy()
        """ Move the viewport by the offset specified """
        self.rect.move_ip(offset[0], offset[1])
        if not self.world_rect.collidepoint(self.rect.center):
            self.rect = oldrect
        
    def move_to(self, position):
        oldrect = self.rect.copy()
        """ Move the viewport to the specified position """
        self.rect.center = position
        if not self.world_rect.collidepoint(self.center):
            self.rect = oldrect