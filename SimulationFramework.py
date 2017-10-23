import FMMFramework as FMM
import random
from Connection import client_hack
from config import vehicle_count
from typing import Union
from numbers import Number

def all_license_plates():
    return ('NH-{}'.format(i) for i in range(vehicle_count))


def get_fuel_level(license_plate: str) -> float:
    return float(FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['fuel_level'])


def set_fuel_level(license_plate: str, fuel_level: Union[str, Number]):
    if float(fuel_level) < .0:
        fuel_level = .0
    elif float(fuel_level) > 100.0:
        fuel_level = 100.0

    vehicle_id = FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['_id']

    FMM.set_vehicle_fields(
        client_hack, vehicle_id, {
            'fuel_level': str(fuel_level),
            'fuel': str(fuel_level)
        }
    )


def set_battery_voltage(license_plate: str,
                        battery_voltage: Union[str, Number]):
    assert .0 <= float(battery_voltage) <= 14.0

    vehicle_id = FMM.get_vehicle_by_license_plate(
        client_hack, license_plate
    )['_id']

    FMM.set_vehicle_fields(
        client_hack, vehicle_id, {
            'battery_voltage': str(battery_voltage),
            'batteryVoltage': str(battery_voltage)
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


if __name__ == '__main__':
    vehicle_id = FMM.get_some_vehicle(client_hack, 'New Hackshire')['_id']



