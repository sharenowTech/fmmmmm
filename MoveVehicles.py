import xml.etree.ElementTree
import FMMFramework as fmm
from Projection import minlon_, minlat_, maxlon_, maxlat_
import SimulationFramework as sim
import random
import threading
import queue
from Connection import client_hack
from Utilities import expand_dict_with_address
from time import sleep


e = xml.etree.ElementTree.parse('map_hackathon_final.osm').getroot()
all_nodes = {
    node.get('id'): {
        'lat': node.get('lat'), 'lon': node.get('lon'),
        'latitude': node.get('lat'), 'longitude': node.get('lon')
    }
    for node in e.findall('node')
}

position_queues = {
    plate: queue.LifoQueue() for plate in sim.all_license_plates()
}

def random_lat_lon_sequence_of_nodes():
    ways = e.findall('way')
    random_way = random.choice(ways)
    return [
        all_nodes[node.get('ref')]
        for node in random_way.findall('nd')
    ]

class QueueWorker(threading.Thread):
    def __init__(self, plate):
        threading.Thread.__init__(self)
        self.plate = plate

    def run(self):
        global position_queues
        if not position_queues[plate].empty():
            client_hack.get_database('fmm').get_collection(
                'vehicle'
            ).find_one_and_update(
                filter={'plate': plate},
                update={
                    '$set': position_queues[plate].get()
                }
            )
            print('moved {} to {}'.format(plate, lat_lon))
            position_queues[plate] = queue.LifoQueue()


while True:
    plate = random.choice(list(sim.all_license_plates()))

    random_way = random_lat_lon_sequence_of_nodes()
    for lat_lon in random_way:
        if minlat_ < float(lat_lon['lat']) < maxlat_ and minlon_ < float(lat_lon['lon']) < maxlon_:
            position_queues[plate].put(lat_lon)
            QueueWorker(plate).start()
            sleep(.1)
        else:
            break

    """
    threading.Thread(
        target=fmm.get_vehicle_collection(client_hack).find_one_and_update,
        kwargs={
            'filter': {'plate': plate},
            'update': {'$set': expand_dict_with_address(random_way[-1])}
        }
    ).start()
    """