#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:30:17 2017

@author: rik
"""

import csv
from datetime import timedelta, datetime, date


class flight:
    def __init__(self):
        self.company = ""
        self.flight = ""
        self.departure = ""
        self.arrival = ""
        self.origin = ""
        self.destination = ""
        self.flight_type = ""
        self.equipment = ""
        self.duration = ""
        self.stops = 0

    def __init__(self, company, flight, departure="", arrival="",
                 origin="", destination="",
                 flight_type="", equipment="",
                 duration="", stops=0):
        self.company = company
        self.flight = flight
        self.departure = departure
        self.arrival = arrival
        self.origin = origin
        self.destination = destination
        self.flight_type = flight_type
        self.equipment = equipment
        self.duration = duration
        self.stops = stops

    def __str__(self):
        desc = "company:" + self.company + " fl:" + self.flight
        desc = desc + " dep:" + str(self.departure)
        desc = desc + " arr:" + str(self.arrival) + " orig:" + self.origin
        desc = desc + " des:" + self.destination + " type:" + self.flight_type
        desc = desc + " eqp:" + self.equipment + " stops:" + str(self.stops)
        desc = desc + " dur:" + str(self.duration)
        return desc

    def get_id(self):
        desc = self.departure.date().isoformat() + self.company + self.flight
        desc = desc + self.origin

        return desc


def load_flights(filename):
    my_data2 = dict()

    with open(filename, 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter=";",
                               quotechar='"')
        my_data = [data for data in data_iter]
        for data in my_data[1:]:
            if len(data) == 0:
                break

            # obtenemos la duration
            t = datetime.strptime(data[8], "%H:%M")
            duration = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

            # flightDate
            flightDate = datetime.strptime(data[7], "%d-%m-%Y")

            # salida
            t = datetime.strptime(data[4], "%H:%M")
            departure = flightDate + timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

            # llegada
            t = datetime.strptime(data[5], "%H:%M")
            arrival = flightDate + timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

            if arrival < departure:
                arrival = arrival + timedelta(days=1)

            # creacion del vuelo
            fl = flight(company=data[0], flight=data[1],
                        departure=departure,
                        arrival=arrival,
                        origin=data[2], destination=data[3],
                        equipment=data[6], stops=0,
                        duration=duration)

            my_data2[fl.get_id()] = fl

    return my_data2
