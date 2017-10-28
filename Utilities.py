import requests
from config import reverse_geocoding_config

def get_address(lat, lon) -> str:
    try:
        response = requests.get(
            reverse_geocoding_config['url'],
            params={
                'format': 'json',
                'accept-language': 'en',
                'lat': str(lat),
                'lon': str(lon),
            }
        )
    except ConnectionError:
        return 'N/A'

    return response.json()['display_name']

def expand_dict_with_address(lat_lon_dict: dict) -> dict:
    lat = lat_lon_dict['lat']
    lon = lat_lon_dict['lon']
    address = get_address(lat, lon)

    return {
        'lat': lat,
        'lon': lon,
        'latitude': lat,
        'longitude': lon,
        'address': address,
        'full_address': address
    }

# tests
if __name__ == '__main__':
    print(get_address(lat="40.7834104", lon="-73.9549902"))
