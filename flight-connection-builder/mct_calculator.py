#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 19:11:23 2018

@author: rik
"""
#from masterData import airport, mct
#from cflights import flight
from datetime import timedelta


class mct_calculation_basic:
    def getMct(self, arrivalFlight, departureFlight):
        return timedelta(minutes = 30)
    
class mct_calculation:
    def __init__(self, airportMaster, mctMaster):
        self.airport = airportMaster
        self.mct = mctMaster
        
    def getType(self, departure, arrival):
        if not departure in self.airport:
            raise ValueError('Aiport ' + departure + ' no definido')
            
        if not arrival in self.airport:
            raise ValueError('Aiport ' + arrival + ' no definido')
            
        if (self.airport[departure].country == self.airport[arrival].country):
            return 'D'
        else:
            return 'I'
        
        
    def getMct(self, arrivalFlight, departureFlight):
        airport = arrivalFlight.destination
        arrival_cia =  arrivalFlight.company
        departure_cia = departureFlight.company 
        
        arrival_type = self.getType(arrivalFlight.origin, arrivalFlight.destination)
        departure_type = self.getType(departureFlight.origin, departureFlight.destination)
        
        #buscamos el MCT
        valid_mct = [x for x in self.mct 
                        if (x.airport == airport and
                            x.cia_arrival == arrival_cia and
                            x.cia_departure == departure_cia and
                            x.type_arrival == arrival_type and
                            x.type_departure == departure_type)]
        if(len(valid_mct) == 0):
            #busqueda del MCT comodin de llegada
            valid_mct = [x for x in self.mct 
                if (x.airport == airport and
                    x.cia_arrival == '*' and
                    x.cia_departure == departure_cia and
                    x.type_arrival == arrival_type and
                    x.type_departure == departure_type)]

            if(len(valid_mct) == 0):
                #busqueda del MCT comodin de salida
                valid_mct = [x for x in self.mct 
                    if (x.airport == airport and
                        x.cia_arrival == arrival_cia and
                        x.cia_departure == '*' and
                        x.type_arrival == arrival_type and
                        x.type_departure == departure_type)]

                if(len(valid_mct) == 0):
                    #busqueda del MCT comodin de salida y llegada
                    valid_mct = [x for x in self.mct 
                        if (x.airport == airport and
                            x.cia_arrival == '*' and
                            x.cia_departure == '*' and
                            x.type_arrival == arrival_type and
                            x.type_departure == departure_type)]

                    if(len(valid_mct) == 0):
                        #busqueda del MCT comodin de salida/llegada y aeropuerto
                        valid_mct = [x for x in self.mct 
                            if (x.airport == '*' and
                                x.cia_arrival == '*' and
                                x.cia_departure == '*' and
                                x.type_arrival == arrival_type and
                                x.type_departure == departure_type)]
                            
                        if(len(valid_mct) == 0):
                            raise ValueError('MCT not found. Airport = ' + airport +
                                          " arrival company = " + arrival_cia +
                                          " departure company = " + departure_cia +
                                          " arrival type = " + arrival_type +
                                          " departure type = " + departure_type )
        
        return valid_mct[0].mct