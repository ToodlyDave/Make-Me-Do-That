from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = MongoClient("mongodb://coolbois:mrtoodles61@cluster0-shard-00-00-uz5v0.mongodb.net:27017,cluster0-shard-00-01-uz5v0.mongodb.net:27017,cluster0-shard-00-02-uz5v0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

client = MongoClient("mongodb://localhost:27017/")


db=client["test"]
# Issue the serverStatus command and print the results
collection = db["student"]

#data = {"name":"Hashim"}
#x = collection.insert_one(data)

x = collection.find_one()
print(x)