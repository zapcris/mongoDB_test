import pymongo
from pymongo import MongoClient



cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
client = MongoClient(cluster)

print(client.list_database_names())

db = client.swarm_production

print(db.list_collection_names())

