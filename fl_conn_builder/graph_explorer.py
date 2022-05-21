#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:42:34 2017

@author: rik
"""

from fl_conn_builder.flight_node import eNodeType
from fl_conn_builder.connection import connListManager


def recursive_explore(node, nro_paths, visited_airport, visited_flights, cn_list):
    if node.__class__.__name__ == "Node":
        if node.val == "end":
            # finaliza un camino correcto
            # print (str(nro_paths) + ":" + str(VisitedAirport))
            if len(visited_flights) > 1:
                cn_list.addConnection(visited_flights)
            return nro_paths + 1
    elif node.__class__.__name__ == "flight_node":
        if not visited_airport:  # En el primer paso, se incluye el airport actual
            visited_airport.append(node.airport)

        if node.type == eNodeType.arrival:
            # Comprobamos el aeropuerto para si ha sido visitado
            if node.airport in visited_airport:
                return nro_paths
            else:
                visited_airport.append(node.airport)

            # incluir flightID
            visited_flights.append(node.id)

    if len(node.edges) > 0:
        for desc in node.edges:
            nro_paths = recursive_explore(desc, nro_paths, visited_airport[:], visited_flights[:], cn_list)
    else:
        raise ValueError('nodo huerfano:' + node.id)

    return nro_paths


# recorre un  grafo estableciendo
def connection_explorer(flightnet, flight_dict, best_connection=False, best_by_date_od=False):
    start = flightnet.get_node("start")

    cnlist = connListManager(flight_dict, best_connection, best_by_date_od)

    nro_caminos = recursive_explore(start, 0, [], [], cnlist)

    return cnlist
