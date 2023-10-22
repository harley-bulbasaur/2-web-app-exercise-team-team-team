from pymongo import MongoClient

client = MongoClient('mongodb://admin:secret@127.0.0.1:27017/')


db = client['task_board']
tasks_collection = db['tasks']

db = client['Users_DataBase']
user_collection = db['users']

def get_users_collection():
    return user_collection

def get_tasks_collection():
    return tasks_collection

def insert_user(username, password, email):
    try:
        user_document = {
            'username': username,
            'password': password,
            'email': email
        }

        user_collection.insert_one(user_document)
        return user_document['_id']

    except Exception as e:
        print(f"An error occurred during user registration: {e}")
        return None  