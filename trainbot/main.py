"""Defines main executable"""

from . import STATION_CODES

def run():
    print('hello world')
    print(STATION_CODES.get("Leeds"))
    print('LDS' in STATION_CODES.values())
