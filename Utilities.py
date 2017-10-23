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

# tests
if __name__ == '__main__':
    print(get_address(lat="40.7834104", lon="-73.9549902"))
