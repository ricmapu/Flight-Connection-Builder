#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 21:59:58 2017

@author: rik
"""

import graph as gr
import cflights
import flight_node
from datetime import timedelta
from collections import defaultdict
from mct_calculator import mct_calculation_basic


def buildGraph(flights=[], mct_calc = None):

    if mct_calc is None:
        mct_calc = mct_calculation_basic()
        
    graph = gr.directedGraph()

    #Obtener todos los aeropuertos    
    airport = set()
    
    #se crea un diccionario de nodos cada aeropuerto para los nodos conexion
    for fl in flights.values():
        airport.add(fl.origin)
        airport.add(fl.destination)
        
    connect_node = defaultdict(set)
        

    #Crear un nodo para cada salida y llegada
    for fl in flights.values():
        
        #creacion de los nodos de salida y llegada del vuelo
        #y union entre los nodos de vuelo
        dep = flight_node.flight_node(fl.flight, fl.departure , fl.origin,
                                      fl.get_id(),
                                      tipo = flight_node.eNodeType.departure)
 
        arr = flight_node.flight_node( fl.flight, fl.arrival, fl.destination,
                                      fl.get_id(),
                                      tipo = flight_node.eNodeType.arrival)

        graph.add_node(dep)
        graph.add_node(arr)        
        graph.add_edge_id(dep.get_id(), arr.get_id())
        
        #por cada nodo de llegada creamos un nodo de conexion en el apto
        #añadiendo el tiempo de conexion y conectandolo con la llegda
        mct_time = timedelta(minutes = 30)
        connect_time = fl.arrival + mct_time
        
        connection_airport = fl.destination
        connection_ready_arr = flight_node.flight_node("", connect_time,
                                                       connection_airport,
                                                       fl.get_id(),
                                                       tipo = flight_node.eNodeType.connection)
        
        graph.add_node(connection_ready_arr)
        connect_node[connection_airport].add(connection_ready_arr.get_id())
        
        graph.add_edge_id( arr.get_id(), connection_ready_arr.get_id())
        
        #por cada nodo de salida creamos un nodo de conexion en el apto
        #conectandolo con la salida
        connection_airport = fl.origin
        connection_ready_dep = flight_node.flight_node("", fl.departure,
                                                       connection_airport,
                                                       fl.get_id(),
                                                       tipo = flight_node.eNodeType.connection)
        
        graph.add_node(connection_ready_dep)
        connect_node[connection_airport].add(connection_ready_dep.get_id())
        graph.add_edge_id(connection_ready_dep.get_id(), dep.get_id())

    #Creación del nodo de inicio y fin
    startNd = gr.Node("start")
    graph.add_node(startNd)
    
    endNd = gr.Node("end")
    graph.add_node(endNd)
    
    for key in connect_node:
        last_node_id = "start"
        for node_id in sorted(connect_node[key]):
            graph.add_edge_id(last_node_id, node_id)
            last_node_id = node_id
        #ultimo nodo, conecta con fin
        graph.add_edge_id(last_node_id, "end")
   
    return graph

def buildGraphTipo2(flights=[], mct_calc = None, maxConnectTime = None):

    if mct_calc is None:
        mct_calc = mct_calculation_basic()

    if maxConnectTime is None:
        maxConnectTime = timedelta(hours = 6)

    graph = gr.directedGraph()
    
    #Creación del nodo de inicio y fin
    startNd = gr.Node("start")
    graph.add_node(startNd)
    
    endNd = gr.Node("end")
    graph.add_node(endNd)
    
    #Obtener todos los aeropuertos    
    airport = set()
    
    #se crea un diccionario de nodos cada aeropuerto para los nodos conexion
    for fl in flights.values():
        airport.add(fl.origin)
        airport.add(fl.destination)
        
    connect_node = defaultdict(set)
        

    #Crear un nodo para cada salida y llegada
    for fl in flights.values():
        
        #creacion de los nodos de salida y llegada del vuelo
        #y union entre los nodos de vuelo
        dep = flight_node.flight_node(fl.flight, fl.departure , fl.origin,
                                      fl.get_id(),
                                      tipo = flight_node.eNodeType.departure)
 
        arr = flight_node.flight_node( fl.flight, fl.arrival, fl.destination,
                                      fl.get_id(),
                                      tipo = flight_node.eNodeType.arrival)

        graph.add_node(dep)
        graph.add_node(arr)        
        graph.add_edge_id(dep.get_id(), arr.get_id())
        
        #por cada nodo de salida creamos una conexion con el nodo start
        #y el nodo departure y la llegada y el nodo arrival
        graph.add_edge_id(startNd.get_id(), dep.get_id())
        graph.add_edge_id(arr.get_id(), endNd.get_id())
        
    #Connectar los vuelos de llegada con los vuelos de salida que conecta
    for fl in flights.values():
        arr = flight_node.flight_node( fl.flight, fl.arrival, fl.destination,
                              fl.get_id(),
                              tipo = flight_node.eNodeType.arrival)
        #buscamos todos lo vuelos que conectan
#        connect_time = fl.arrival + timedelta(minutes = 30)
#        fl_connections = [x for x in flights.values() if (x.departure >= connect_time and x.origin == fl.destination)]
        fl_connections = [x for x in flights.values() 
                                    if (fl.destination == x.origin and x.departure<= fl.arrival + maxConnectTime and x.departure >= (fl.arrival +mct_calc.getMct(fl, x)))
                         ]
         
        for fl_connect in fl_connections:
            dep = flight_node.flight_node(fl_connect.flight, 
                                          fl_connect.departure , 
                                          fl_connect.origin,
                                          fl_connect.get_id(),
                                          tipo = flight_node.eNodeType.departure)
            graph.add_edge_id(arr.get_id(), dep.get_id())

        
    #Conexiones de los nodos start y end    
    for key in connect_node:
        last_node_id = "start"
        for node_id in sorted(connect_node[key]):
            graph.add_edge_id(last_node_id, node_id)
            last_node_id = node_id
        #ultimo nodo, conecta con fin
        graph.add_edge_id(last_node_id, "end")
   
    return graph
    