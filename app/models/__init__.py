from sqlalchemy import Table, Column, ForeignKey, Integer, String,\
Boolean, Text, DateTime, func
from sqlalchemy.orm import relationship, backref, deferred
from app.database import Base, db_session
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

TIMESTRING = "%Y-%m-%dT%H:%M:%S"

class User(Base):
  #Custom attribute to define user selectable fields since
  #optional field selection will be allowed for all API
  user_fields = [
    "id", 
    "uname", 
    "email", 
    "password"
  ]
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  uname = Column(String(32), unique=True)
  email = Column(String(64), unique=True)
  password = deferred(Column(String(60)))
  enabled = deferred(Column(Boolean, default=True))


  def __repr__(self):
    return '< User(uname: %s, email: %s, enabled: %s) >' %\
      (self.uname, self.email, self.enabled)

  #Required methods for flask user login
  def get_id(self):
    return unicode(self.id)

  def is_active(self):
    return self.enabled

  def is_anonymouse(self):
    return False

  def is_authenticated(self):
    return True
