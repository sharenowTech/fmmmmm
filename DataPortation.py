import pymongo.database
import random
import datetime


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
        'hardwareVersion': "HW3"
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


def manipulate_vehicle_fields(client: pymongo.MongoClient,
                              vehicle_id: str,
                              update: dict):

    client.get_database('fmm').get_collection('vehicle').find_one_and_update(
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

    client.get_database('fmm').get_collection('vehicle').find_one_and_update(
        {'_id': vehicle_id},
        {'$set': update_date}
    )

def get_random_vehicle_id(client: pymongo.MongoClient,
                          location_name: str):
    location_id = get_location_id(client, location_name)
    vehicles = client.get_database('fmm').get_collection('vehicle').find({
        'locationId': location_id
    })
    return vehicles[random.randint(0, vehicles.count()-1)]['_id']


# unit-tests
if __name__ == '__main__':
    pass