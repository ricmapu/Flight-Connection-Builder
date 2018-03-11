#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:42:34 2017

@author: rik
"""

import graph as gr
from flight_node import flight_node, eNodeType
from connection import connectionList, connection, connListManager

   
def recursive_explore(node, nro_paths, VisitedAirport, VisitedFlights, cnList):
    
    if node.__class__.__name__ == "Node":        
        if node.val == "end":
            #finaliza un camino correcto
            #print (str(nro_paths) + ":" + str(VisitedAirport))
            if len(VisitedFlights) > 1:
                cnList.addConnection(VisitedFlights)
            return  nro_paths + 1
    elif node.__class__.__name__ == "flight_node":
        if VisitedAirport == []: #En el primer paso, se incluye el airport actual
            VisitedAirport.append(node.airport)
      
        if node.type == eNodeType.arrival:
            #Comprobamos el aeropuerto para si ha sido visitado
            if node.airport in VisitedAirport:
                return  nro_paths 
            else:
                VisitedAirport.append(node.airport)
                
            #incluir flightID
            VisitedFlights.append(node.id)

    if len(node.edges) > 0:         
        for desc in node.edges:
            nro_paths = recursive_explore(desc, nro_paths, VisitedAirport[:], VisitedFlights[:], cnList)
    else:
        raise ValueError('nodo huerfano:' + node.id)
  
    return nro_paths
        

#recorre un  grafo estableciendo
def connection_explorer(flightnet, flightDict, bestConnection = False, bestByDateOD = False ):
        
    start = flightnet.get_node("start")
    
    cnlist = connListManager(flightDict, bestConnection, bestByDateOD)
    
    nro_caminos = recursive_explore(start, 0, [], [],  cnlist)
    
    return cnlist


