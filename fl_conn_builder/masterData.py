# -*- coding: utf-8 -*-
import csv
from datetime import timedelta


class airport:
    def __init__(self, iatacode="", country=""):
        self.iatacode = iatacode
        self.country = country


class mct:
    def __init__(self, airport, cia_arrival, cia_departure,
                 type_arrival, type_departure, mct):
        self.airport = airport
        self.cia_arrival = cia_arrival
        self.cia_departure = cia_departure
        self.type_arrival = type_arrival
        self.type_departure = type_departure
        self.mct = mct


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
            horas = int(data[5][0:2])
            minutos = int(data[5][3:5])
            maxconnect_time = timedelta(minutes=horas * 60 + minutos)

            mct_dict.append(mct(airport, cia_arrival, cia_departure,
                                type_arrival, type_departure, maxconnect_time))

    return mct_dict
