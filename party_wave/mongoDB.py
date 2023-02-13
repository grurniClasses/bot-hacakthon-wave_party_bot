from pymongo import MongoClient

def connect_database():
  client = MongoClient()
  db = client.get_database("partywave")
  return db

