import random
import FMMFramework as FMM
from Utilities import get_address
from Connection import client_int, client_hack


def random_coordinates_from_hackathon_location():
    minlat, maxlat = 40.7497, 40.7687
    minlon, maxlon = -73.9916, -73.9656
    lat = str(random.uniform(minlat, maxlat))
    lon = str(random.uniform(minlon, maxlon))
    address = get_address(lat, lon)

    return {
        'lat': lat,
        'latitude': lat,
        'lon': lon,
        'longitude': lon,
        'full_address': address,
        'address': address
    }


def import_e_smart_into_hackathon_location(license_plate: str):
    some_e_smart = FMM.get_some_e_smart(client_int, 'Stuttgart')

    some_e_smart['plate'] = license_plate
    some_e_smart['numberPlate'] = license_plate
    some_e_smart['phone_from_bo'] = '+49 30 233 40 110'
    some_e_smart['phoneNumber'] = '+49 30 233 40 110'

    some_e_smart.update(random_coordinates_from_hackathon_location())

    FMM.import_vehicle(client_hack, 'New Hackshire', some_e_smart)



if __name__ == '__main__':
    for i in range(0, 15):
        # import 15 vehicles into hackathon location
        # import_e_smart_into_hackathon_location('NH-{}'.format(i))
        pass



