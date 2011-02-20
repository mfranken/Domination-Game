DEFAULT_AMMO_PACKS = 10 #number of ammo packs when the game starts
AMMO_SPAWN_PROB = 0.2 #chance of ammo spawning every ai step
WORLD_SIZE = (1000, 1000)
AMMO_PER_PACK = 3
WALLS = [
         #outside walls
         ((3, 3), (1, 994)),
         ((3, 3), (994, 1)),
         ((997, 3), (1, 994)),
         ((3, 997), (994, 1)),
         #clover cuts
         ((3, 499), (350, 3)),
         ((499, 3), (3, 350)),
         ((647, 499), (350, 3)),
         ((499, 647), (3, 350))]
BLUE_SPAWN_POINT = (40, 40)
RED_SPAWN_POINT = (960, 960)
CONTROL_POINTS = [(500,500), (100,900), (900,100)] #control points in the game
PLAYERS_PER_TEAM = 10 #number of players per team
RESPONSE_TIME = 3 #seconds in which every agent should respond
DEFAULT_AMMO = 0 #number of shots a player can do after spawning
