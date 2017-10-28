from os.path import join
from bson.json_util import dumps
from Connection import client_hack
import os

user_dir = os.path.expanduser('~')

def backup_db(backup_db_dir):
    client = client_hack
    for database_name in client.database_names():
        database = client.get_database(database_name)
        collections = database.collection_names()
        for i, collection_name in enumerate(collections):
            col = getattr(database,collections[i])
            collection = col.find()
            jsonpath = database_name + '/' + collection_name + ".json"
            jsonpath = join(backup_db_dir, jsonpath)
            with open(jsonpath, 'w+') as jsonfile:
                jsonfile.write(dumps(collection))

if __name__ == '__main__':
    backup_db(os.path.join(user_dir, 'hackathon_mongo_backup'))