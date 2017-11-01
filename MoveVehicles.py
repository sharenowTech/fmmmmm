import xml.etree.ElementTree
import FMMFramework as fmm
from Projection import minlon_, minlat_, maxlon_, maxlat_
import SimulationFramework as sim
import random
import threading
import queue
import time
from config import vehicle_count
from Connection import client_hack
from Utilities import expand_dict_with_address


map = xml.etree.ElementTree.parse('map_hackathon_final.osm').getroot()
nodes = {
    node.get('id'): {
        'lat': node.get('lat'), 'lon': node.get('lon'),
        'latitude': node.get('lat'), 'longitude': node.get('lon')
    }
    for node in map.findall('node')
}

ways = [
    [
        nodes[node.get('ref')]
        for node in way.findall('nd')
    ]
    for way in map.findall('way')
]

plates = list(sim.all_license_plates())

position_queues = {
    plate: queue.LifoQueue() for plate in sim.all_license_plates()
}

max_simulated_paths = 10

class QueueWorker(threading.Thread):
    def __init__(self, plate):
        threading.Thread.__init__(self)
        self.plate = plate

    def run(self):
        if not position_queues[self.plate].empty():
            lat_lon = position_queues[self.plate].get()
            client_hack.get_database('fmm').get_collection(
                'vehicle'
            ).find_one_and_update(
                filter={'plate': self.plate},
                update={
                    '$set': lat_lon
                }
            )
            print('moved {} to {}'.format(self.plate, lat_lon))
            position_queues[self.plate] = queue.LifoQueue()


class PositionProducer(threading.Thread):
    def __init__(self, plate):
        threading.Thread.__init__(self)
        self.plate = plate

    def run(self):
        for _ in range(max_simulated_paths):
            random_way = random.choice(ways)
            for lat_lon in random_way:
                if minlat_ < float(lat_lon['lat']) < maxlat_ and minlon_ < float(lat_lon['lon']) < maxlon_:
                    position_queues[self.plate].put(lat_lon)
                    QueueWorker(self.plate).start()
                    time.sleep(1.0)
                else:
                    break


def main():
    # TODO: choose a way containing the node the car was located last
    vehicle_threads = {
        plate: PositionProducer(plate)
        for plate in sim.all_license_plates()
    }

    for thread in vehicle_threads.values():
        thread.start()

    for thread in vehicle_threads.values():
        thread.join()


if __name__ == '__main__':
    main()