DEFAULT_AMMO_PACKS = 10 #number of ammo packs when the game starts
AMMO_SPAWN_PROB = 0.2 #chance of ammo spawning every ai step
WORLD_SIZE = (1000, 1000)
AMMO_PER_PACK = 3
WALLS = [((3, 3), (1, 994)),
         ((3, 3), (994, 1)),
         ((997, 3), (1, 994)),
         ((3, 997), (994, 1))]
BLUE_SPAWN_POINT = (40, 40)
RED_SPAWN_POINT = (960, 960)
CONTROL_POINTS = [(500,500), (300,700), (700,300)] #control points in the game
PLAYERS_PER_TEAM = 10 #number of players per team
RESPONSE_TIME = 3 #seconds in which every agent should respond
DEFAULT_AMMO = 0 #number of shots a player can do after spawning
