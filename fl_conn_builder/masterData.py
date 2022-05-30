# -*- coding: utf-8 -*-
import csv
from datetime import timedelta
from dataclasses import dataclass
import pandas as pd


@dataclass
class airport:
    iatacode: str
    country: str


@dataclass
class mct:
    airport: str
    cia_arrival: str
    cia_departure: str
    type_arrival: str
    type_departure: str
    mct: timedelta


def load_airports(filename):
    airport_dict = dict()

    with open(filename, 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter=",",
                               quotechar='"')
        my_data = [data for data in data_iter]
        for data in my_data[1:]:
            iatacode = data[0]
            country = data[1]

            airport_dict[iatacode] = airport(iatacode, country)

    return airport_dict


def load_mct(filename):
    mct_dict = list()

    with open(filename, 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter=",",
                               quotechar='"')

        my_data = [data for data in data_iter]
        for data in my_data[1:]:
            airport = data[0]
            cia_arrival = data[1]
            cia_departure = data[2]
            type_arrival = data[3]
            type_departure = data[4]
            hours = int(data[5][0:2])
            minutes = int(data[5][3:5])
            maxconnect_time = timedelta(minutes=hours * 60 + minutes)

            mct_dict.append(mct(airport, cia_arrival, cia_departure,
                                type_arrival, type_departure, maxconnect_time))

    return mct_dict


def load_mct_cirium(filename):
    mct_dict = list()

    xls_file = pd.read_excel(filename, sheet_name='OAG', skiprows=1, dtype=str)

    for index, row in xls_file.iterrows():
        airport = row.values[1]
        cia_arrival = row.values[5]
        cia_departure = row.values[10]
        type_arrival = row.values[3][0:1]
        type_departure = row.values[3][1:2]
        hours = int(row.values[4][0:2])
        minutes = int(row.values[4][2:4])
        maxconnect_time = timedelta(minutes=hours * 60 + minutes)

        mct_dict.append(mct(airport, cia_arrival, cia_departure,
                            type_arrival, type_departure, maxconnect_time))

    return mct_dict
