"""Compute complex attractors of asynchronous Boolean networks.

Copyright (C) 2022 giang.trinh91@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import IO

import networkx as nx
import matplotlib.pyplot as plt

from pyeda.boolalg import boolfunc
from pyeda.boolalg.bdd import bddvar, expr2bdd
from pyeda.boolalg.expr import expr

from typing import List, Set

"""
A python package for approximating minimum feedback vertex sets
"""
from FVSpython3 import FVS as FVS

"""
List of nodes
"""
nodes = []

"""
List of Boolean functions
"""
bdd_funs = {}

"""
Unsigned interaction graph
"""
ig = nx.DiGraph()

"""
Signed interaction graph
"""
signed_ig = nx.DiGraph()

"""
IN(x): list of input nodes of node x
"""
INx = {}

"""
List of source nodes
"""

source_nodes = []

def get_control_nodes(ig: nx.DiGraph, scc: List[str]) -> List[str]:
    controls = []

    for n in scc:
        preds = ig.predecessors(n)

        for pred in preds:
            controls.append(pred)

    controls = list(set(controls) - set(scc))

    return controls 

def get_ig():
    """Build the unsigned interaction graph"""
    for x in nodes:
        ig.add_node(x)

        for y in INx[x]:
            ig.add_edge(str(y), str(x))

def get_signed_ig():
    """Build the signed interaction graph"""
    for x in nodes:
        signed_ig.add_node(x)

        for y in INx[x]:
            signed_ig.add_edge(str(y), str(x), weight=0)

def set_retained_set(U: List[str]):
    B = {}

    for x in U:
        B[x] = 0

def read_network_structure(fileobj: IO):
    """Parse a BoolNet .bnet file and get static information."""

    for line in fileobj.readlines():
        if line.startswith("#") or line.startswith("targets, factors"):
            continue
        try:
            x, fx = line.replace(" ", "").replace("!", "~").split(",", maxsplit=1)
        except ValueError:  # not enough values to unpack
            continue
             
        nodes.append(x)

        if fx.strip() == x:
            source_nodes.append(x)

        fx = expr(fx) # Boolean function in form of pyeda.boolalg.expr

        INx[x] = fx.support # list of nodes appearing in Boolean function fx

        #fx = expr2bdd(expr(fx)) # Boolean function in form of pyeda.boolalg.bdd

        #bdd_funs[x] = fx
            
    get_ig()

    #print("|S| = " + str(len(source_nodes)))

def compute_attractor():
    """Find feedback vertex set"""
    U = FVS.FVS(ig)
    #print("|U| = " + str(len(U)))
    print("|U-| = " + str(len(U) - len(source_nodes)))
    print(" ".join(U))

    #get_signed_ig()

    #set_retained_set(U)

    
