from pymongo import MongoClient

client = MongoClient('mongodb://admin:secret@127.0.0.1:27017/')


db = client['task_board']
tasks_collection = db['tasks']


def get_tasks_collection():
    return tasks_collection
