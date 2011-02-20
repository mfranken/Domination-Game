"""Parse command line arguments."""
import os, sys
import getopt

def get_options():
  """
  Return options dictionary according to commandline.
  """
  short_opts = 'hb:r:l:o:c:p:i'
  long_opts = ['help','blue=','red=','level=','output=','record=','replay=','invisible']

  try:
    opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
  except getopt.GetoptError:
    usage()
    sys.exit(1)

  # Check commandline options
  options = {}
  for opt, arg in opts:
    if opt in ('-h','--help'):
      usage()
      sys.exit(0)
    if opt in ('-b','--blue'):
      options['blue'] = arg
    if opt in ('-r','--red'):
      options['red'] = arg
    if opt in ('-o', '--ouput'):
      options['output'] = arg
    if opt in ('-l', '--level'):
      options['level'] = arg
    if opt in ('-c', '--record'):
      options['record'] = arg
    if opt in ('-p', '--replay'):
      options['replay'] = arg
    if opt in ('-i', '--invisible'):
      options['invisible'] = True

  # Set defaults where necessary.
  if options.has_key('replay'):
    options['record'] = False
    options['blue'] = options['red'] = 'replay_agent'
    if not os.path.exists(options['replay']):
        print 'Replay file does not exist.'
        sys.exit(1)
    options['invisible'] = False
  else:
    options['replay'] = False
    
    if not options.has_key('blue'):
      print 'Using default Blue brain: claiming_agent'
      options['blue'] = 'claiming_agent'

    if not options.has_key('red'):
      print 'Using default Red brain: claiming_agent'
      options['red'] = 'claiming_agent'

    if not options.has_key('record'):
      options['record'] = False

    if not options.has_key('level'):
      print 'Using default level: default'
      options['level'] = 'default'
      
    if not options.has_key('invisible'):
      options['invisible'] = False
        
  if not options.has_key('output'):
    print 'Using default output file: output'
    options['output'] = 'output'
    
    
  return options

def usage():
  """ Print usage info. """

  use = """
domination.py -r blocking_agent -b claiming_agent -l default -o output -c replay
domination.py -p replay -o output

Arguments:
  -h, --help
    This help text.

  -b <name>, --blue=<name>
    Name of the brain, located in the brains folder, to use for the
    Blue Team.

  -r <name>, --red=<name>
    Name of the brain, located in the brains folder, to use for the
    Red Team.
  
  -l <name>, --level=<name>
    Name of the level, located in the levels folder.
    
  -o <name>, --level=<name>
    Name of the output file where the score is written. First the blue score,
    then the red, seperated by a space.
  
  -c <name>, --record=<name>
    Name of the file to save the replay as.
  
  -p <name>, --replay=<name>
    Name of the replay file to play. Ignores agent choices, level and invisible options.
    
  -i, --invisible
    Do not show the GUI. Speeds up the simulation.
"""
  print use
