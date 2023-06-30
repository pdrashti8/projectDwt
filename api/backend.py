from pymongo import MongoClient
import json
from flask import Flask, jsonify, request
import pvFunctions as func
from bson import ObjectId
import datetime


app = Flask(__name__)

#----------------- CRUD for User Profile -----------------
# need to add check for unique email id
@app.route('/create_profile', methods=['POST'])
def create_profile():
    
    db = func.mongodb_conn()
    user_collection = db['user']

    data = request.json
        
    # Extract the values from the data dictionary
    Fname = data['firstName']
    Lname = data['lastName']
    Email = data['email']
    Password = func.hash_password(data['password'])

    # Set current date and time
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    createdOn = current_datetime_str
    editedOn = current_datetime_str

    # Check for unique Email in a user collection
    if func.email_exists(Email):
        return jsonify({'error': 'Email already exists'}), 400

    # Create the user document
    document = {
        'firstName': Fname,
        'lastName': Lname,
        'email': Email,
        'password': Password,
        'createdOn': createdOn,
        'editedOn': editedOn
    }

     # Insert the document into the collection
    result = user_collection.insert_one(document)

     # Return the inserted document (with ObjectId converted to string)
    inserted_document = user_collection.find_one({"_id": result.inserted_id})
    inserted_document['_id'] = str(inserted_document['_id'])  # Convert ObjectId to string
    
    # Disconnect from MongoDB
    func.mongodb_disconn()
    
    return jsonify(inserted_document)


#  Read user profile
@app.route('/user/<email>', methods=['GET'])
def user_profile(email):

    # Establish a connection to MongoDB
    db = func.mongodb_conn()
    user_collection = db['user'] 

    # Query the collection for the document with the specified email
    user = user_collection.find_one({'email': email})

    # Close the MongoDB connection
    func.mongodb_disconn()

    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})


@app.route('/edit_profile', methods=['POST'])
def edit_profile():

    db = func.mongodb_conn()
    user_collection = db['user'] 

    # Get the data from the request
    data = request.json

    # Extract the fields from the data
    Fname = data['firstName']
    Lname = data['lastName']
    Email = data['email']
    Password = func.hash_password(data['password'])

    # Set edited date and time
    edited_datetime = datetime.datetime.now()
    edited_datetime_str = edited_datetime.strftime("%Y-%m-%d %H:%M:%S")
    editedOn = edited_datetime_str

    # Create the update query
    query = {'email': Email}
    update = {
        '$set': {
            'firstName': Fname,
            'lastName': Lname,
            'password': Password,
            'editedOn': editedOn
        }
    }

    # Update the document
    result = user_collection.update_one(query, update)

    if result.modified_count > 0:
        # Disconnect from MongoDB
        func.mongodb_disconn()
        return 'Profile updated successfully'
    else:
        # Disconnect from MongoDB
        func.mongodb_disconn()
        return (f'No Profile found with {Email} Email ID')


@app.route('/delete_profile', methods=['DELETE'])
def delete_profile():
    db = func.mongodb_conn()
    user_collection = db['user']

    # Get the data from the request
    data = request.json
    Email = data['email']

    print('Recently deleted Profile with ---------',Email)
    result = user_collection.delete_one({'email': Email})

     # Disconnect from MongoDB
    func.mongodb_disconn()
    
    if result.deleted_count == 1:
        return f"User with emailId {Email} deleted successfully"
    else:
        return f"User with emailId {Email} not found"
    

#----------------- CRUD for Project -----------------

@app.route('/create_proj', methods=['POST'])
def create_proj():
    
    db = func.mongodb_conn()
    user_collection = db['user']
    proj_collection = db['project']

    data = request.json
        
    # Extract the values from the data dictionary
    Email = data['email']
    ProjName = data['projName']

    isActive = 1

    # Set current date and time
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    createdOn = current_datetime_str
    editedOn = current_datetime_str

    # Get userID of the user from user collection
    user = user_collection.find_one({'email': Email})
    if user:
        user['_id'] = str(user['_id'])
        UserId = user['_id']
    else:
        return f"User with emailId {Email} not found"
    


    # Create the project document
    document = {
        'userId': UserId,
        'projName': ProjName,
        'isActive': isActive,
        'createdOn': createdOn,
        'editedOn': editedOn
    }

     # Insert the document into the collection
    result = proj_collection.insert_one(document)

     # Return the inserted document (with ObjectId converted to string)
    inserted_document = proj_collection.find_one({"_id": result.inserted_id})
    inserted_document['_id'] = str(inserted_document['_id'])  # Convert ObjectId to string
    
    # Disconnect from MongoDB
    func.mongodb_disconn()
    
    return jsonify(inserted_document)


#  Read all Projects of a User
@app.route('/projects/<email>', methods=['GET'])
def get_proj(email):

    # Establish a connection to MongoDB
    db = func.mongodb_conn()
    user_collection = db['user']
    proj_collection = db['project']

    # Query for specified userID
    user = user_collection.find_one({'email': email})
    if user:
        user['_id'] = str(user['_id'])
        UserId = user['_id']
    else:
        return f"User with emailId {email} not found"
    
    # Query for projects with the specified userID
    projects = proj_collection.find({'userId': UserId})

    
    # Convert the cursor to a list of dictionaries
    projects_list = list(projects)
    print(projects_list)

    # Close the MongoDB connection
    func.mongodb_disconn()

    if projects_list:
        for i in projects_list:
            i['_id'] = str(i['_id'])
        return jsonify(projects_list)
    else:
        return jsonify({'error': 'No projects found'})


@app.route('/edit_proj', methods=['POST'])
def edit_proj():

     # Extract the fields from the data
    data = request.json
    Email = data['email']
    ProjName = data['projName']
    isActive = data['isActive']
    
    # Set edited date and time
    edited_datetime = datetime.datetime.now()
    edited_datetime_str = edited_datetime.strftime("%Y-%m-%d %H:%M:%S")
    editedOn = edited_datetime_str

    # Establish a connection to MongoDB
    db = func.mongodb_conn()
    user_collection = db['user']
    proj_collection = db['project']

    # Query for specified userID
    user = user_collection.find_one({'email': Email})
    if user:
        user['_id'] = str(user['_id'])
        UserId = user['_id']
    else:
        return f"User with emailId {Email} not found"
    
    # Query for projects with the specified userID
    proj = proj_collection.find_one({'userId': UserId, 'projName': ProjName})
    if proj:
        projId = proj['_id']
    else:
        return jsonify({'error': 'Project not found'})
    
    # Create the update query
    query = {'_id': projId}
    update = {
        '$set': {
            'projName': ProjName,
            'isActive': isActive,
            'editedOn': editedOn
        }
    }

    # Update the document
    result = proj_collection.update_one(query, update)

    if result.modified_count > 0:
        # Disconnect from MongoDB
        func.mongodb_disconn()
        return 'Profile updated successfully'
    else:
        # Disconnect from MongoDB
        func.mongodb_disconn()
        return (f'No Project found for {Email} Email ID with {ProjName} Project Name')
    

@app.route('/delete_proj', methods=['DELETE'])
def delete_proj():

      # Extract the fields from the data
    data = request.json
    Email = data['email']
    ProjName = data['projName']

    db = func.mongodb_conn()
    user_collection = db['user']
    proj_collection = db['project']

    # Query for specified userID
    user = user_collection.find_one({'email': Email})
    if user:
        user['_id'] = str(user['_id'])
        UserId = user['_id']
    else:
        # Disconnect from MongoDB
        func.mongodb_disconn()

        return f"User with emailId {Email} not found"
    
    # Query for projects with the specified userID
    proj = proj_collection.find_one({'userId': UserId, 'projName': ProjName})
    if proj:
        result = proj_collection.delete_one({'_id': proj['_id']})

        # Disconnect from MongoDB
        func.mongodb_disconn()

        if result.deleted_count == 1:
            return f"Project {ProjName} deleted successfully"
        else:
            return f"Error while deleting the Project"

    else:
        # Disconnect from MongoDB
        func.mongodb_disconn()

        return jsonify({'error': 'Project not found'})

    
    
    
    








if __name__ == '__main__':
    app.run()

