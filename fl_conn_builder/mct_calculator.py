#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 19:11:23 2018

@author: rik
"""
# from masterData import airport, mct
# from cflights import flight
from datetime import timedelta


class mct_calculation_basic:
    def get_mct(self, arrival_flight, departure_flight):
        return timedelta(minutes=30)

    def get_intercity_airport(self, l_airport):
        connected_airport = list()

        connected_airport.append(l_airport)

        return connected_airport


class mct_calculation:
    def __init__(self, airport_master, mct_master):
        self.airport = airport_master
        self.mct = mct_master

    def get_type(self, departure, arrival):
        if departure not in self.airport:
            raise ValueError('Aiport ' + departure + ' no definido')

        if arrival not in self.airport:
            raise ValueError('Aiport ' + arrival + ' no definido')

        if self.airport[departure].country == self.airport[arrival].country:
            return 'D'
        else:
            return 'I'

    def get_mct(self, arrival_flight, departure_flight):
        arrival_station = arrival_flight.destination
        arrival_cia = arrival_flight.airline_designator
        departure_cia = departure_flight.airline_designator
        departure_station = departure_flight.origin

        arrival_type = self.get_type(arrival_flight.origin, arrival_flight.destination)
        departure_type = self.get_type(departure_flight.origin, departure_flight.destination)

        # buscamos el MCT
        valid_mct = [x for x in self.mct
                     if (x.arrival_station == arrival_station and
                         x.departure_station == departure_station and
                         x.cia_arrival == arrival_cia and
                         x.cia_departure == departure_cia and
                         x.type_arrival == arrival_type and
                         x.type_departure == departure_type)]
        if len(valid_mct) == 0:
            # busqueda del MCT comodin de llegada
            valid_mct = [x for x in self.mct
                         if (x.arrival_station == arrival_station and
                             x.departure_station == departure_station and
                             x.cia_arrival == '*' and
                             x.cia_departure == departure_cia and
                             x.type_arrival == arrival_type and
                             x.type_departure == departure_type)]

            if len(valid_mct) == 0:
                # busqueda del MCT comodin de salida
                valid_mct = [x for x in self.mct
                             if (x.arrival_station == arrival_station and
                                 x.departure_station == departure_station and
                                 x.cia_arrival == arrival_cia and
                                 x.cia_departure == '*' and
                                 x.type_arrival == arrival_type and
                                 x.type_departure == departure_type)]

                if len(valid_mct) == 0:
                    # busqueda del MCT comodin de salida y llegada
                    valid_mct = [x for x in self.mct
                                 if (x.arrival_station == arrival_station and
                                     x.departure_station == departure_station and
                                     x.cia_arrival == '*' and
                                     x.cia_departure == '*' and
                                     x.type_arrival == arrival_type and
                                     x.type_departure == departure_type)]

                    if len(valid_mct) == 0:
                        # busqueda del MCT comodin de salida/llegada y aeropuerto
                        valid_mct = [x for x in self.mct
                                     if (x.arrival_station == '*' and
                                         x.departure_station == '*' and
                                         x.cia_arrival == '*' and
                                         x.cia_departure == '*' and
                                         x.type_arrival == arrival_type and
                                         x.type_departure == departure_type)]

                        if len(valid_mct) == 0:
                            raise ValueError('MCT not found. arrival_station = ' + arrival_station +
                                             " departure_station = " + arrival_station +
                                             " arrival company = " + arrival_cia +
                                             " departure company = " + departure_cia +
                                             " arrival type = " + arrival_type +
                                             " departure type = " + departure_type)

        return valid_mct[0].mct

    def get_intercity_airport(self, l_airport):
        connected_airport = list()

        valid_dep = [x.departure_station for x in self.mct
                     if (x.arrival_station == l_airport )]

        connected_airport = list(set(valid_dep))

        return connected_airport
