import math, random
from math import pi, sqrt, pow
import pygame, settings

class AgentBrain():
    """ Control point hugger! """
    agent_no = 1
    def __init__(self):
        self.no = AgentBrain.agent_no
        AgentBrain.agent_no += 1       
    
    def action(self, observation):
        """ Set the new action parameters.
        The student's code should be called here.
        """
        action = {
            'turn': random.random()*pi/1.5 - pi/3,
            'speed': 50,
            'shoot': False
        }
        
        self.go_to_control_point(observation,action)    
                
        #print "\n"
        #print self.no
        #print observation        
        self.get_ammo_when_empty(observation,action)            
        self.shoot_enemy(observation,action)  
            
        self.move_random_when_close_to_wall(observation,action)

            
        return action
        
    def distance_to_wall(self,location, walls):                
    # approximation! get's distance to closest corner
        distance_to_corners = []
        for wall in walls:            
            distance_to_corners.append(self.distance_between_points(location,(wall['bottom'],wall['top'])))
            distance_to_corners.append(self.distance_between_points(location,(wall['left'],wall['top'])))
            distance_to_corners.append(self.distance_between_points(location,(wall['right'],wall['bottom'])))
            distance_to_corners.append(self.distance_between_points(location,(wall['left'],wall['right'])))
        return min(distance_to_corners)
            
    def distance_between_points(self,x,y):
        return sqrt( pow(abs(x[0]-y[0]),2) + pow(abs(x[1]-y[1]),2) )
        
    def angle_between_points(self,x,y):
        return math.atan2(y[1] - x[1], y[0] - x[0] )
        
    def get_closest(self,list,location):
        if list == []:
            return "None"
        closest = (99999,99999)
        shortest_dist = 9999999
        for element in list:
            if self.distance_between_points(element,location) < shortest_dist:
                closest = element
                shortest_dist = self.distance_between_points(element,location)
        return closest
        
    def get_closest_enemy(self,agents,own_team_color, own_location):
        enemies = []
        for agent in agents:
            if agent['team'] != own_team_color:
                enemies.append((agent['location'][0],agent['location'][1]))
        closest_enemy = self.get_closest(enemies,own_location)
        return closest_enemy
        
    def shoot_enemy(self,observation,action):
        # Shoot enemy
        # if you have ammo
        if observation['ammo'] != 0:
            # and there is and agent spotted
            if observation['agents'] != []: 
                # and there is a closest enemy
                closest_enemy = self.get_closest_enemy(observation['agents'],observation['team'],observation['location'])
                if closest_enemy != "None":
                    if self.distance_between_points(closest_enemy ,observation['location']) < settings.MAX_SHOT_DISTANCE:                        
                        action['turn'] = -1 * observation['direction'] + self.angle_between_points(observation['location'],closest_enemy)
                        action['shoot'] = True
                        action['speed'] = 0
        
    def move_random_when_close_to_wall(self,observation,action):
        # If close to a wall move randomly
        if observation['walls'] != []:
            if self.distance_to_wall(observation['location'],observation['walls']) < 50:
                action['turn'] = random.random()*pi/1.5 - pi/3
                action['speed'] = 50                

    def get_ammo_when_empty(self,observation,action):
        # Get ammo if empty
        if observation['ammo'] == 0:
            # add ammopacks to list
            ammopack_locations = []
            for ammopack in observation['ammopacks']:
                ammopack_locations.append(ammopack['location'])
            closest_ammopack = self.get_closest(ammopack_locations,observation['location'])
            if closest_ammopack != "None":
                action['turn'] = -1 * observation['direction'] + self.angle_between_points(observation['location'],closest_ammopack)
                         
    def go_to_control_point(self,observation,action):
        if observation['controlpoints'] != []:
            # Go to closest control point which is not in possession
            controlpoints_not_in_possession = []
            for controlpoint in observation['controlpoints']:
                if controlpoint['team'] != observation['team']:
                    controlpoints_not_in_possession.append(controlpoint['location'])
            closest_controlpoint_not_in_possession = self.get_closest(controlpoints_not_in_possession,observation['location'])
            if closest_controlpoint_not_in_possession != "None":
                action['turn'] = -1 * observation['direction'] + self.angle_between_points(observation['location'],closest_controlpoint_not_in_possession)
                action['speed'] = 50
            # Otherwise go to a control point and defend it        
            else:
                visible_controlpoints = []
                for controlpoint in observation['controlpoints']:
                    visible_controlpoints.append(controlpoint['location'])
                closest_controlpoint = self.get_closest(visible_controlpoints,observation['location'])
                action['turn'] = -1 * observation['direction'] + self.angle_between_points(observation['location'],closest_controlpoint)
                action['speed'] = 10           
       