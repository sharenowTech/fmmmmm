import FMMFramework as FMM
import random
from Connection import client_hack
from config import vehicle_count
from typing import Union, Generator
from numbers import Number


def all_license_plates() -> Generator:
    return ('NH-{}'.format(i) for i in range(vehicle_count))


def get_fuel_level(license_plate: str) -> float:
    return float(FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['fuel_level'])


def set_fuel_level(license_plate: str, fuel_level: Union[str, Number]):
    fuel_level = float(fuel_level)
    if fuel_level < .0:
        fuel_level = .0
    elif fuel_level > 100.0:
        fuel_level = 100.0

    vehicle_id = FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['_id']

    FMM.set_vehicle_fields(
        client_hack, vehicle_id, {
            'fuel_level': '{:.4}'.format(fuel_level),
            'fuel': '{:.4f}'.format(fuel_level)
        }
    )


def set_battery_voltage(license_plate: str,
                        battery_voltage: Union[str, Number]):
    battery_voltage = float(battery_voltage)
    assert .0 <= battery_voltage <= 14.0

    vehicle_id = FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['_id']

    FMM.set_vehicle_fields(
        client_hack, vehicle_id, {
            'battery_voltage': '{:.3f}'.format(battery_voltage),
            'batteryVoltage': '{:.3f}'.format(battery_voltage)
        }
    )


def revive_12v_battery(license_plate: str):
    set_battery_voltage(license_plate, random.uniform(12.0, 14.0))


def kill_12v_battery(license_plate: str):
    new_battery_voltage = random.uniform(0.0, 11.6)
    set_battery_voltage(license_plate, new_battery_voltage)


def drain_fuel(license_plate: str, drain: Union[str, Number]):
    old_fuel_level = get_fuel_level(license_plate)
    new_fuel_level = max(old_fuel_level-float(drain), .0)
    set_fuel_level(license_plate, new_fuel_level)


def get_tasks_for_vehicle(license_plate: str):
    return FMM.get_tasks(
        client_hack,
        {
            'vehicleId': FMM.get_vehicle_by_license_plate(client_hack,
                                                          license_plate)
        }
    )


def delete_tasks_for_vehicle(license_plate: str):
    vehicle_id = FMM.get_vehicle_by_license_plate(client_hack,
                                                  license_plate)['_id']
    FMM.delete_tasks(client_hack, {'vehicleId': vehicle_id})


if __name__ == '__main__':
    plate = 'NH-0'
    """
    vehicle = FMM.get_vehicle_by_license_plate(client_hack, 'NH-0')
    print(get_fuel_level(plate))
    print(set_fuel_level(plate, 120))
    print(get_fuel_level(plate))
    print(get_tasks_for_vehicle(plate))
    """
    # delete_tasks_for_vehicle(plate)
    print([task for task in get_tasks_for_vehicle(plate)])
    # kill_12v_battery(plate)
    revive_12v_battery(plate)
    # delete_tasks_for_vehicle(plate)







