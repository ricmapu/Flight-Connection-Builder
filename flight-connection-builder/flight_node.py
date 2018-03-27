# -*- coding: utf-8 -*-
import graph
from enum import Enum, auto

class eNodeType(Enum):
    departure = auto()
    arrival = auto()
    connection = auto()

class flight_node(graph.Node):
    def __init__(self, flight, time, airport, fl_id, tipo = eNodeType.connection):
        self.flight = flight
        self.time = time
        self.airport = airport
        self.type = tipo
        self.id = fl_id
        self.edges = []
        
        return
    
    def get_id(self):
        id_str =  self.time.isoformat() +"_" + self.airport + "_" + self.flight +"_"  + str(self.type)
        
        return id_str
    
    def __str__(self):
        return 
        

