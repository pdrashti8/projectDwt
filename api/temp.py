from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Use the database and collection
db = client['dwt']
user_collection = db['user']

# Create the document
document = {
    'userId': 1,
    'Fname': 'Drashti',
    'Lname': 'Patel',
    'Email': 'test@gmail.com',
    'Password': '1234',
    'projects': ['Dubai', 'China', 'Singapore']
}

# Insert the document into the collection
user_collection.insert_one(document)
print("document inserted!!!")
# Disconnect from MongoDB
client.close()