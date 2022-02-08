# required imports
from os import getenv
from urllib.parse import urlparse
from telethon.crypto import AuthKey
from telethon.sessions import MemorySession
from pymongo import MongoClient

class MongoSession(MemorySession):
  """Telethon PyMongo Session
    
    By Jonathan Irhodia (https://elcharitas.com.ng)

    This session contains the required information to login into your
    Telegram account. If you think the session has been compromised, close all the sessions
    through an official Telegram client to revoke the authorization.
  """
  
  _auth_key = None

  DB = MongoClient(getenv("DB_URL")).get_database("sketchstorm")

  def cursor(self, key):
    return self.DB.get_collection(key)

  def set_dc(self, dc_id, server_address, port):
    super().set_dc(dc_id, server_address, port)
    if data := self.cursor("sessions").find_one(dc_id):
      self._auth_key = AuthKey(data=data)

  def get_update_state(self, entity_id):
    return self._update_states.get(entity_id, None)

  def set_update_state(self, entity_id, state):
    self._update_states[entity_id] = state

  def find(self, key, attr = None):
    return self.cursor(key).find(attr)
