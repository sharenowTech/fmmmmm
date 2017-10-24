import SimulationFramework as sim
import numpy as np
import threading
import random
from time import sleep
from queue import Queue
from typing import List, Callable

action_queues = {
    plate: Queue()
    for plate in sim.all_license_plates()
}


class QueueWorker(threading.Thread):
    def __init__(self, queue: Queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                return
            else:
                action = self.queue.get()
                """
                try:
                    execute_action(action)
                except:
                    break
                """
                if __debug__:
                    print('Executing action {} with args {}.'.format(
                        action[0].__name__, action[1]
                    ))
                execute_action(action)


def execute_action(action):
    action[0](*action[1])


def app_opening_periodic(propability: float):
    for plate in sim.all_license_plates():
        if random.random() < propability:
            # TODO: write app opening code
            pass


def drain_fuel_periodic(min_drain: float, max_drain: float):
    for plate in sim.all_license_plates():
        action_queues[plate].put(
            [sim.drain_fuel, [plate, random.uniform(min_drain, max_drain)]]
        )
    start_workers()

    if __debug__:
        print('drained fuel [{:.4f}, {:.4f}] from vehicles'.format(min_drain,
                                                                   max_drain))


def kill_battery_periodic(propability: float):
    for plate in sim.all_license_plates():
        if random.random() < propability:
            action_queues[plate].put(
                [sim.kill_12v_battery, [plate]]
            )
            if __debug__:
                print('Killed battery of {}.'.format(plate))
    start_workers()


def initialize_simulation():
    for plate in sim.all_license_plates():
        action_queues[plate].put(
            [sim.set_fuel_level, [plate, 100]]
        )

        action_queues[plate].put(
            [sim.revive_12v_battery, [plate]]
        )

        action_queues[plate].put(
            [sim.delete_tasks_for_vehicle, [plate]]
        )
    start_workers()
    if __debug__:
        print('Initialized Simulation.')


def start_workers():
    for plate in sim.all_license_plates():
        QueueWorker(action_queues[plate]).start()


def is_finished_simulation() -> bool:
    # TODO: define a condition which actually makes sense
    return False


def simulation_step(step_frequency: float=1.0):
    """
    perfoms 1 simulation step on fmm
    :param step_frequency: number of simulation steps per second
    :return:
    """

    # time lapsed between simulation steps in seconds
    time_per_step = 1.0 / step_frequency
    drain_fuel_periodic(0.5*time_per_step/100.0, 1.5*time_per_step/100.0)

    # kill battery about once per hour
    kill_battery_periodic(time_per_step/3600.0)



def main():
    step_frequency = 1.0
    initialize_simulation()
    # simulation loop
    while not is_finished_simulation():
        simulation_step()
        sleep(1.0/step_frequency)



if __name__ == '__main__':
    main()
