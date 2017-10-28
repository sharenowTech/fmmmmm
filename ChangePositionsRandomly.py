import FMMFramework as fmm
import SimulationFramework as sim
import random
import threading
from Connection import client_hack
from time import sleep

while True:
    plate = random.choice(list(sim.all_license_plates()))
    vehicle = fmm.get_vehicle_by_license_plate(client_hack, plate)
    vehicle.update(sim.random_coordinates_from_hackathon_location())
    threading.Thread(
        target=fmm.set_vehicle_fields,
        kwargs={
            'client': client_hack,
            'vehicle_id': vehicle['_id'],
            'update': vehicle
        }
    ).start()
    sleep(1)
