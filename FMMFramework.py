import pymongo.database
import random
import datetime
import requests
from typing import List


def get_vehicle_collection(client: pymongo.MongoClient
                           ) -> pymongo.database.Collection:
    return client.get_database('fmm').get_collection('vehicle')


def get_location_id(client: pymongo.MongoClient, location_name: str):
    return client.get_database('common').get_collection('location').find_one({
        'name': location_name
    })['_id']


def get_some_e_smart(from_client: pymongo.MongoClient,
                     from_location: str) -> dict:
    e_smart_query = {
        'locationId': get_location_id(
            from_client, from_location
        ),
        'model': "SMART", 'engine_type': "ED",
        'status': "green",
        'hardwareVersion': "HW3",
        'has_damages': 'false',
        'hasDamages': 'false'
    }

    e_smarts = (
        from_client.get_database('fmm').get_collection('vehicle').find(
            e_smart_query
        )
    )

    return e_smarts[random.randint(0, e_smarts.count()-1)]


def import_vehicle(to_client: pymongo.MongoClient,
                   to_location: str,
                   vehicle: dict):
    to_location_id = get_location_id(to_client, to_location)
    vehicle['locationId'] = to_location_id
    to_client.get_database('fmm').get_collection('vehicle').insert(vehicle)


def import_e_smart(from_client: pymongo.MongoClient,
                   from_location: str,
                   to_client: pymongo.MongoClient,
                   to_location: str):

    some_e_smart = get_some_e_smart(from_client, from_location)
    import_vehicle(to_client, to_location, some_e_smart)


def get_vehicle_fields(client: pymongo.MongoClient,
                       vehicle_id: str,
                       keys: list):
    vehicle = get_vehicle_by_id(client, vehicle_id)
    return {key: vehicle[key] for key in keys}


def set_vehicle_fields(client: pymongo.MongoClient,
                       vehicle_id: str,
                       update: dict):
    get_vehicle_collection(client).find_one_and_update(
        {'_id': vehicle_id},
        {'$set': update}
    )
    update_last_change_date(client, vehicle_id)



def update_last_change_date(client: pymongo.MongoClient,
                            vehicle_id: str):
    update_date = {
        'lastChangeDate': datetime.datetime.utcnow(),
        'lastCABAUpdateDate': datetime.datetime.utcnow()
    }

    get_vehicle_collection(client).find_one_and_update(
        {'_id': vehicle_id},
        {'$set': update_date}
    )


def get_some_vehicle(client: pymongo.MongoClient,
                     location_name: str) -> dict:
    location_id = get_location_id(client, location_name)
    vehicles = get_vehicle_collection(client).find({
        'locationId': location_id
    })
    return vehicles[random.randint(0, vehicles.count()-1)]


def get_vehicle_by_id(client: pymongo.MongoClient, vehicle_id: str) -> dict:
    return get_vehicle_collection(client).find_one({'_id': vehicle_id})


def get_vehicle_by_license_plate(client: pymongo.MongoClient,
                                 license_plate: str) -> dict:
    return get_vehicle_collection(client).find_one(
        filter={
            'plate': license_plate,
            'numberPlate': license_plate
        }
    )


def get_tasks(client: pymongo.MongoClient, filter: dict=None):
    return client.get_database('fmm').get_collection('task').find(
        filter if filter is not None else None
    )

def get_task(client: pymongo.MongoClient, task_id):
    return client.get_database('fmm').get_collection('task').find_one(
        {'_id': task_id}
    )

def create_task(client: pymongo.MongoClient,
                task_type: dict,
                vehicle_id: str,
                location_id: str,
                user_id: str,
                url: str,
                access_token: str,
                additional_fields: dict=None):
    task = {
        'vehicleId': vehicle_id,
        'vehicle_comment': None,
        'assignedTo': None,
        'assigned': None,
        'status': 'OPEN',
        'locationId': location_id,
        'followOn': False,
        'createdBy': pymongo.database.ObjectId(user_id),
        'photos': [],
        'activities': [],
        'created': datetime.datetime.utcnow(),
        'disregardStatus': False,
        'taskType': [task_type],
        'comments': [],
    }

    if additional_fields is not None:
        task.update(additional_fields)

    client.get_database('fmm').get_collection('task').insert(
        task
    )

    requests.get(
        url=url+'/protected/vehicles/syncByVehicleId/'+str(vehicle_id),
        headers={'accessToken': access_token, 'userId': user_id}
    )



def assign_task_to_vehicle(client: pymongo.MongoClient,
                           task_id):
    pass

def delete_tasks(client: pymongo.MongoClient, filter: dict):
    client.get_database('fmm').get_collection('task').delete_many(filter)

# unit-tests
if __name__ == '__main__':
    from Connection import client_hack
    for task in get_tasks(client_hack):
        print(task)
