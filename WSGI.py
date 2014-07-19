from app import app
from run import get_configs

if __name__ == "__main__":
  host, port, debug = get_configs()
  app.run(host=host, port=port, debug=debug)