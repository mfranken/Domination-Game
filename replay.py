import shelve, utils

REPLAY = None
REPLAY_TURN = 0

def start(path, level):
    """
    Start recording. Also, saves the state of the random generator.
    """
    global REPLAY
    REPLAY = shelve.open(path, writeback=True)
    REPLAY['level'] = level
    REPLAY['random_state'] = utils.RANDOM.getstate()

def end():
    """
    Ends recording/replaying. Failing to call this will result in a
    corrupted replay.
    """
    global REPLAY
    if REPLAY != None:
        REPLAY.close()

def step():
    """
    Notifies the replay that a turn has passed.
    """
    global REPLAY_TURN
    REPLAY_TURN += 1
    
def record(id, team, action):
    """
    Records an action.
    """
    global REPLAY
    if REPLAY == None:
        return
    # Remove labels to save some space
    action_copy = action.copy()
    if action_copy.has_key('label'):
        del action_copy['label']
    # Store action in replay file
    key = '%s.%s.%s' % (REPLAY_TURN, team, id)
    REPLAY[key] = action_copy

def open(path):
    """
    Open a replay for replaying (not for recording).
    """
    global REPLAY
    REPLAY = shelve.open(path, writeback=True)
    return REPLAY['level'], REPLAY['random_state']
    
def replay(id, team):
    """
    Recalls an action from the replay.
    """
    key = '%s.%s.%s' % (REPLAY_TURN, team, id)
    if not REPLAY.has_key(key):
        print "Error: '%s' not found in replay" % key
        return {}
    return REPLAY[key]
