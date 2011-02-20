DEFAULT_AMMO_PACKS = 8 #number of ammo packs when the game starts
AMMO_SPAWN_PROB = 0.2 #chance of ammo spawning every ai step
WORLD_SIZE = (800, 800)
AMMO_PER_PACK = 3
WALLS = [
         #outside walls
         ((3, 3),   (1, 794)),
         ((3, 3),   (794, 1)),
         ((797, 3), (1, 794)),
         ((3, 797), (794, 1)),
	   #clover cuts
         ((300, 100), (3, 200)),
         ((100, 300), (203, 3)),
	   ((300, 500), (3, 200)),
         ((100, 500), (203, 3)),
	   ((600, 400), (197, 3)),
	   ((600, 200), (3,400))
	   ]
	   
BLUE_SPAWN_POINT = (643, 360)
RED_SPAWN_POINT = (643, 440)
CONTROL_POINTS = [(500,400), (220,220), (220,580)] #control points in the game
PLAYERS_PER_TEAM = 8  #number of players per team
RESPONSE_TIME = 1 #seconds in which every agent should respond
DEFAULT_AMMO = 0 #number of shots a player can do after spawning
