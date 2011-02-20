import replay

class AgentBrain():
    def __init__(self):
        # There, sadly, is no easier way to get to the command line options
        from commandline import get_options
        options = get_options()
        replay.open(options['replay'])
        
    def action(self, observation):
        return replay.replay(observation['id'], observation['team'])
