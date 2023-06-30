from pymongo import MongoClient
import bcrypt

# ------------ Database connection functions ---------

def mongodb_conn():
    try:
        global client
        client = MongoClient('mongodb://localhost:27017/')
        client.server_info()  # will raise an exception if failed
        print("Connected to MongoDB successfully..........!!!")

        db = client['dwt']

    except Exception as e:
        print("******  Failed to connect to MongoDB:", str(e), "******")
        db = "******  Failed to connect to MongoDB:", str(e), "******"
    
    return db

def mongodb_disconn():
    try:
        if client:
            client.close()
            print("Disconnection successful..........!!!")
    except Exception as e:
        print("******  Disconnection failed:", str(e), "******")


# ------------ Password Hash function ---------
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password = str(hashed_password)
    return hashed_password


# ------------ Validate Password ---------
def verify_password(password, hashed_password):
    # Verify the password against the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# ------------ Check for unique Email ------------
def email_exists(email):
     
    db = mongodb_conn()
    user_collection = db['user']

    # Query the collection for the email
    user = user_collection.find_one({'email': email})

    mongodb_disconn()

    return user is not None