import SimulationFramework as sim
import numpy as np
import threading
from queue import Queue
from typing import List, Callable

class QueueWorker(threading.Thread):
    def __init__(self, queue: Queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            else:
                execute_action(self.queue.get())


action_queues = {
    plate: Queue()
    for plate in sim.all_license_plates()
}


def execute_action(action):
    action[0](*action[1])


def initialize_simulation():
    for plate in sim.all_license_plates():
        action_queues[plate].put(
            [sim.set_fuel_level, [plate, 90]]
        )

        action_queues[plate].put(
            [sim.revive_12v_battery, [plate]]
        )

        action_queues[plate].put(
            [sim.delete_tasks_for_vehicle, [plate]]
        )


def create_workers() -> dict:
    return {
        plate: QueueWorker(action_queues[plate])
        for plate in sim.all_license_plates()
    }


def start_workers():
    for plate in sim.all_license_plates():
        QueueWorker(action_queues[plate]).start()


def is_finished_simulation() -> bool:
    return True

def simulation_step(time_scale: float=1.0):
    """
    perfoms 1 simulation step on fmm
    :param time_scale: number of simulation steps per second
    :return:
    """
    pass

def main():
    initialize_simulation()
    start_workers()

    # simulation loop
    while not is_finished_simulation():
        simulation_step()
        start_workers()
        

if __name__ == '__main__':
    main()