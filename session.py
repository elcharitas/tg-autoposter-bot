# required imports
import datetime
from os import getenv
from urllib.parse import urlparse
from telethon import types
from telethon.crypto import AuthKey
from telethon.sessions import MemorySession
from pymongo import MongoClient

from constants import DB_URL, DB_NAME, DB_SESS

class MongoSession(MemorySession):
  """Telethon PyMongo Session
    
    By Jonathan Irhodia (https://elcharitas.com.ng)

    This session contains the required information to login into your
    Telegram account. If you think the session has been compromised, close all the sessions
    through an official Telegram client to revoke the authorization.
  """
  
  _auth_key: AuthKey = None

  _conn: MongoClient = None

  def __init__(self, key=None, conn: MongoClient = MongoClient(DB_URL)):
    super().__init__()

    # setup defaults
    self._conn = conn
    self.id = key
    self.DB = self._conn.get_database(DB_NAME)

  def cursor(self, key: str = DB_SESS):
    """Creates a cursor for interacting with a collection

    Args:
        key (str, optional): The name of the collection to get cursor for. Defaults to DB_SESS.

    Returns:
        Collection: The cursor for our mongodb collection
    """
    return self.DB.get_collection(key)

  def find(self, attr: dict = None):
    return [MongoSession(session.id, conn=self._conn) for session in self.cursor().find(attr)]

  def init(self, id):
    return MongoSession(id, conn=self._conn)
  
  def get_update_state(self, entity_id):
    return self.cursor("sessions").find_one({ "id": entity_id })

  def process_entities(self, tlo):
    self._entities = self.find()

  def set_dc(self, dc_id, server_address, port):
    super().set_dc(dc_id, server_address, port)
    if data := self.cursor().find_one({"auth_key": dc_id}):
      self._auth_key = AuthKey(data=data)
