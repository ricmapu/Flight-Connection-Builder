#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:22:14 2017

@author: rik
"""

import csv
from datetime import date

class connection:
    def __init__(self, flights = []):
        self.flight = flights
        if len(flights) > 0:
            self.duration = flights[-1].arrival - flights[0].departure
            self.origin = flights[0].origin
            self.destination = flights[-1].destination
            
    def getId(self, by_date_origin_destination = False):
        if not by_date_origin_destination:
            if len(self.flight):
                ls_id =self.flight[0].get_id() + "_" + self.destination
            else:
                ls_id =""
        else:#by origin_destination_day
            if len(self.flight):
                ls_id =self.flight[0].departure.date().isoformat()  + "_" + self.origin + "_" + self.destination
            else:
                ls_id =""
            
            
        return ls_id
    
    def get_duration(self):
        return self.duration
    
    def get_nro_flights(self):
        return len(self.flight)
    
class connectionList:
    def __init__(self, bestConnection = False, bestByDateOD = False):
        self.bestConnection = bestConnection
        self.bestByDateOD = bestByDateOD        
  
        if self.bestConnection:
            self.connections = dict()
        else:
            self.connections = list()
        
    def add(self, connection):
        if self.bestConnection:
            cn_id = connection.getId(self.bestByDateOD)
            if cn_id not in self.connections:
                self.connections[cn_id] = connection
            else:
                if self.connections[connection.getId(self.bestByDateOD)].get_duration() > connection.get_duration():
                    self.connections[cn_id]= connection
        else:
            self.connections.append(connection)
            
    def getList(self):
        if self.bestConnection:
            return list(self.connections.values())
        else:
            return self.connections[:]

    def getmaxnroflights(self):
        #Max nro mde conexiones
        max_nro_flights = 0
        for conn in self.getList():
            nro_flights = conn.get_nro_flights()
            if nro_flights > max_nro_flights:
                max_nro_flights = nro_flights
        
        return max_nro_flights


class connListManager:
    def __init__(self, flightDict, bestConnection = False, bestByDateOD = False):
        self.fl = flightDict
        self.connectionList = connectionList(bestConnection, bestByDateOD)
        
    def addConnection(self, fl_id_list):
        #Buscamos los vuelos a partir del ID y creamos una conexion
        fl_list = [self.fl[x] for x in fl_id_list]
        fl_path = connection(fl_list)
        
        self.connectionList.add(fl_path)
        
    def getmaxnroflights(self):
        #Max nro mde conexiones
        return self.connectionList.getmaxnroflights()
    
        
    def saveCsv(self, filename):  
        maxnroflights = self.getmaxnroflights()
        names =['id', 'date', 'origin', 'destination', 'steps', 'duration']
        
        for flrow in range(maxnroflights):
                    names = names + [ "date"+str(flrow) , "flight"+str(flrow),
                                   "origin"+str(flrow), "destination"+str(flrow),
                                   "departure"+str(flrow), "arrival"+str(flrow),
                                   "duration"+str(flrow)]
        
        with open(filename, 'w') as csvfile:
            csv_iter = csv.writer(csvfile, delimiter = ",", quotechar = '"')
            
            csv_iter.writerow(names)
            for row in self.connectionList.getList():
                data = [row.getId(),
                        row.flight[0].departure.strftime("%Y-%m-%d"),
                        row.flight[0].origin,
                        row.flight[-1].destination, 
                        row.get_nro_flights(), row.get_duration()]
            
                for fl in row.flight:
                    data = data + [fl.departure.strftime("%Y-%m-%d") ,
                                   fl.company + fl.flight,
                                   fl.origin, fl.destination,
                                   fl.departure, fl.arrival,
                                   fl.duration]
                    
                csv_iter.writerow(data)
        