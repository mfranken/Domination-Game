from game_object import GameObject
import pygame, utils
from settings import *

class AmmoPack(GameObject):
    layer = 2
    
    def __init__(self, world):
        GameObject.__init__(self)
        self.world = world
        self.image = pygame.image.load('graphics/ammo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        #spawn at random location
        while True:
            self.rect.center = (
                utils.RANDOM.gauss(0.5,0.2)*self.world.level.WORLD_SIZE[0],
                utils.RANDOM.gauss(0.5,0.35)*self.world.level.WORLD_SIZE[1])
            if len(self.world.touching_objects(self)) == 0:
                break
    
    def update(self):
        for a in self.world.touching_objects(self):
            try:
                a.ammo += self.world.level.AMMO_PER_PACK
            except (AttributeError):
                print a, "is not capable of picking up ammo"
            self.kill()