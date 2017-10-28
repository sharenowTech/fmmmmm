import FMMFramework as FMM
import SimulationFramework as sim
from Connection import client_int, client_hack
from SimulationFramework import random_coordinates_from_hackathon_location


def import_e_smart_into_hackathon_location(license_plate: str):
    some_e_smart = FMM.get_some_e_smart(client_int, 'Stuttgart')

    some_e_smart.update(random_coordinates_from_hackathon_location())

    FMM.import_vehicle(client_hack, 'New Hackshire', some_e_smart)

    remove_sensitive_vehicle_data(some_e_smart['_id'], license_plate)


def remove_sensitive_vehicle_data(vehicle_id, license_plate: str):
    vehicle = FMM.get_vehicle_by_id(client_hack, vehicle_id)

    vehicle.update(
        {
            'plate': license_plate,
            'numberPlate': license_plate,
            'vin': license_plate,
            'exterior': 'GOOD',
            'interior': 'GOOD',
            'exteriorCleanliness': [],
            'interiorCleanliness': [],
            'statusChangeReason': '',
            'ip_from_bo': '0.0.0.0',
            'has_damages': 'false',
            'hasDamages': 'false',
            'ipAdress': '0.0.0.0',
            'phone_from_bo': '+49 30 233 40 110',
            'phoneNumber': '+49 30 233 40 110',
            'remarks': '',
            'mileage': "0",
            'operationStateComment': '',
            'initialRegistrationDate': '2017-10-27',
            'smartMXId': license_plate,
            'iccid': license_plate,
            'rfidVehicleKey': license_plate,
            'rfidFuelcard': license_plate,
            'rfidParkingcard': license_plate,
        }
    )

    FMM.get_vehicle_collection(client_hack).replace_one(
        {'_id': vehicle_id},
        vehicle
    )


def import_charging_station(charging_station: str, lon_lat: dict):
    station = FMM.get_some_e_smart(client_int, 'Stuttgart')
    station['plate'] = charging_station
    station['numberPlate'] = charging_station
    station['locationAlias'] = 'newhack'
    station['status'] = 'blue'
    station.update(lon_lat)
    FMM.import_vehicle(client_hack, 'New Hackshire', station)
    remove_sensitive_vehicle_data(FMM.get_vehicle_by_license_plate(
        client_hack, charging_station
    )['_id'], charging_station)


if __name__ == '__main__':
    for i in range(10):
        sim.create_charging_station_task('charging station {}'.format(i))


