import sys
from app import *
from ConfigParser import ConfigParser

def get_configs():
  config = ConfigParser()
  config.read('config.ini')
  if bool(config.get('development', 'enabled')):
    server_type = 'development'
    debug = True
  else:
    server_type = 'production'
    debug = False
  return (config.get(server_type, 'host'),
          int(config.get(server_type, 'port')),
          debug)

if len(sys.argv) == 1:
  host, port, debug = get_configs()
  app.run(host=host, port=port, debug=debug)
else:
  #Use this to setup the DB
  if sys.argv[1] == 'setup':
      from app.database import *
      kill_db()
      init_db()
      setup_db()
      sys.exit()
  #Use this to setup python shell
  elif sys.argv[1] == 'shell':
    from flask import *
    from app import *
    from app.models import *
    from IPython import embed
    embed()
    sys.exit()

sys.exit()
