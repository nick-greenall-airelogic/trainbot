import csv

from .resources import STATION_CODE_CSV

with open(STATION_CODE_CSV) as file_handle:
    file_reader = csv.reader(file_handle)
    STATION_CODES = {rows[0]: rows[1] for rows in file_reader}
