from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ConfigParser import ConfigParser
import os.path

def get_created_engine():
  config = ConfigParser()
  config.read(os.path.dirname(__file__) + '/../config.ini')
  #For development, we will use a sqlite database
  if bool(config.get('development', 'enabled')):
    db_string = 'sqlite:///%s' % config.get('development', 'sqlite_db')
    return create_engine(db_string, echo=True)
  prod = 'production'
  #Generate database string based on configuration file (mysql)
  db_string = 'mysql://%s:%s@%s:%s/%s' % (config.get(prod, 'mysql_user'),
                                          config.get(prod, 'mysql_pass'),
                                          config.get(prod, 'mysql_host'),
                                          config.get(prod, 'mysql_port'),
                                          config.get(prod, 'mysql_db'))
  return create_engine(db_string, echo=False)

engine = get_created_engine()
db_session = scoped_session(sessionmaker(autocommit=False, 
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from app.models import *

def init_db():
    Base.metadata.create_all(engine)

def kill_db():
    Base.metadata.drop_all(engine)

def setup_db():
    #from app.models import *
    import app.models as models
    """User Creation
    """
    user = models.User(uname='user', email='user@user.com', password='123456')
    db_session.add(user)
    db_session.commit()
