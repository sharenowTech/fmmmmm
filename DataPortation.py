import pymongo.database
import random
import datetime

def get_location_id(client: pymongo.MongoClient, location_name: str):
    return client.get_database('common').get_collection('location').find_one({
        'name': location_name
    })['_id']


def import_e_smart(from_client: pymongo.MongoClient,
                   from_location: str,
                   to_client: pymongo.MongoClient,
                   to_location: str):

    e_smart_query = {
        'locationId': get_location_id(
            from_client, from_location
        ),
        'model': "SMART", 'engine_type': "ED",
        'status': "green",
        'hardwareVersion': "HW3"}

    e_smart = (
        from_client.get_database('fmm').get_collection('vehicle').find_one(
            e_smart_query)
    )

    to_location_id = get_location_id(
        to_client, to_location
    )

    e_smart['locationId'] = to_location_id

    to_client.get_database('fmm').get_collection('vehicle').insert(e_smart)


def manipulate_vehicle_field(client: pymongo.MongoClient,
                             vehicle_id: str,
                             update: dict):
    _update = update.copy()
    _update.update({
        'lastChangeDate': datetime.datetime.utcnow(),
        'lastCABAUpdateDate': datetime.datetime.utcnow()
    })

    client.get_database('fmm').get_collection('vehicle').find_one_and_update(
        {'_id': vehicle_id},
        {'$set': _update}
    )


def get_random_vehicle_id(client: pymongo.MongoClient,
                          location_name: str):
    location_id = get_location_id(client, location_name)
    vehicles = client.get_database('fmm').get_collection('vehicle').find({
        'locationId': location_id
    })
    return vehicles[random.randint(0, vehicles.count()-1)]['_id']






if __name__ == '__main__':
    from Connection import client_hack
    print(get_location_id(client_hack, 'New Hackshire'))
    vehicle_id = get_random_vehicle_id(client_hack, 'New Hackshire')
    print(vehicle_id)
    manipulate_vehicle_field(
        client_hack, vehicle_id,
        {'battery_voltage': '8.000', 'batteryVoltage': '8.000'}
    )
