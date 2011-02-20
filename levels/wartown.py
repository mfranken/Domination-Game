DEFAULT_AMMO_PACKS = 10 #number of ammo packs when the game starts
AMMO_SPAWN_PROB = 0.2 #chance of ammo spawning every ai step
WORLD_SIZE = (1000, 500)
AMMO_PER_PACK = 3
WALLS = [((3, 3), (1, 494)),
         ((3, 3), (994, 1)),
         ((997, 3), (1, 494)),
         ((3, 497), (994, 1)),
         #around first cp
         ((3, 120), (140, 4)),
         ((120, 40), (4, 140)),
         #around second cp
         ((475, 350), (4, 120)),
         ((525, 350), (4, 120)),
         ((460, 380), (130, 4)),
         #around third cp
         ((650, 125), (120, 4)),
         ((675, 20), (4, 120)),
         #in the middle
         ((300, 250), (120, 4)),
         ((400, 140), (4, 120))]
BLUE_SPAWN_POINT = (40, 250)
RED_SPAWN_POINT = (960, 250)
CONTROL_POINTS = [(100,100), (500,400), (700,100)] #control points in the game
PLAYERS_PER_TEAM = 10 #number of players per team
RESPONSE_TIME = 3 #seconds in which every agent should respond
DEFAULT_AMMO = 0 #number of shots a player can do after spawning
