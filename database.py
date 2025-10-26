# Copied from MongoDB Atlas Cloud after creating cluster except: db = client["blogdb"], collection = db["posts"].

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection string
uri = "mongodb+srv://emon51:11235813@emon.kzdyaew.mongodb.net/?appName=emon"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Choose (or create) the database
db = client["blogdb"]

# Choose (or create) the collection
collection = db["posts"]

# Optional: Test the connection (You can omit it later)
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)

