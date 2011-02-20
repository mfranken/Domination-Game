#!/usr/bin/env python
import pygame, threading, time, replay, utils
from pygame.locals import *
from viewport import Viewport
from world import World
from settings import *
import commandline

#pygame initialization
pygame.init()
KEYS_EVENT = USEREVENT + 1
pygame.time.set_timer(KEYS_EVENT, 10)

class Domination:
    """ Initializes the game. Keeps track of events. """
    def __init__(self, options):
        self.options = options
        
        if options['record']:
            replay.start(options['record'], options['level'])
        elif options['replay']:
            options['level'], rand_state = replay.open(options['replay'])
            utils.RANDOM.setstate(rand_state)
        self.output_file = options['output']
        self.viewport = Viewport()
        self.world = World(options['red'], options['blue'], options['level'])
        self.viewport.set_world(self.world)
        self.running = True
        self.world_lock = threading.Lock()
 
    def game_loop(self):
        step = 0
        while(self.running):
            #if the world lock is set, only update the GUI, don't move agents.
            if self.world_lock.acquire(False):
                self.on_simulation_step()
                if step % SIMULATION_RESOLUTION == 0:
                    threading.Thread(target=self.on_action).start()
                    #on_action will release the lock after all agents have
                    #declared their action or the time ran out.
                else:
                    self.world_lock.release()
                step += 1
                replay.step()
            
            for event in pygame.event.get():
                self.on_event(event)
                
            self.on_render()
                
            if step > MAX_TIMESTEPS:
                self.running = False
            
        self.on_cleanup()
        
    def on_event(self, event):
        if event.type == KEYS_EVENT:
            self.on_keys()
        if event.type == VIDEORESIZE:
            self.viewport.resize(event.size)
        if event.type == QUIT:
            self.running = False
    
    def on_action(self):
        self.world.action_step()
        self.world_lock.release()

    def on_keys(self):
        move_speed = 10
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.viewport.move_offset((0,-move_speed))
        if keys[K_RIGHT]:
            self.viewport.move_offset((move_speed,0))
        if keys[K_DOWN]:
            self.viewport.move_offset((0,move_speed))
        if keys[K_LEFT]:
            self.viewport.move_offset((-move_speed,0))
        
        if ((keys[K_RALT] or keys[K_LALT]) and keys[K_F4]) or keys[K_ESCAPE]:
            self.running = False
 
    def on_simulation_step(self):
        self.world.simulation_step()
    
    def on_render(self):
        if not self.options['invisible']:
            self.world.render(self.viewport)
            pygame.display.update()
        
    def on_cleanup(self):
        replay.end()
        self.world.cleanup()
        with open(self.output_file, "w") as f:
            for team in self.world.teams:
                f.write(str(team) + "\n")
        
        pygame.quit()

if __name__ == "__main__" :
    #print "actually here"
    options = commandline.get_options()
    dom = Domination(options)
    dom.game_loop()
