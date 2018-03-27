#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 21:54:43 2017

@author: rik
"""

class Node:
    def __init__(self, val):
        self.val = val
        self.edges = []
        
    def get_id(self):
        return str(self.val)

class directedGraph:
    def __init__(self):
        self.nodes = dict()

    def add_node(self, newNode):
        #añade el nodo siempre y cuando no exista ya (evitar dupes)
        key = newNode.get_id()
        if not (key in self.nodes):
            self.nodes[key] = newNode
            
    def get_node(self, ids):
        return self.nodes[ids]

    def add_edge(self, node1, node2):
        node1.edges.append(node2)

    def add_edge_id(self, node1_id, node2_id):
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        self.add_edge(node1, node2)
        
    def node_count(self):
        return len(self.nodes)
    
    def edge_count(self):
        edge_count = 0
        for key,nod in self.nodes.items():
            edge_count += len(nod.edges)
            
        return edge_count
            