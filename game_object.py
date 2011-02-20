import pygame

class GameObject(pygame.sprite.DirtySprite):
    """ Any object in the world: agents, walls, spawn points, control points """
    layer = 0 #draw on background
    collide = False #do not collide
    
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.Rect(0,0,0,0)
        self.image = None
    

    def update(self):
        print type(self)
        raise NotImplementedError()

class Wall(GameObject):
    layer = 3
    collide = True
    
    def __init__(self, location, size):
        GameObject.__init__(self)
        self.rect = pygame.Rect(location, size)
        self.image = pygame.Surface(size)
        self.image.fill(pygame.Color('black'))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
    
    def update(self):
        pass