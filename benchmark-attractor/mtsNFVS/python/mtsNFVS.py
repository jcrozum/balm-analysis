"""Compute complex attractors of an asynchronous Boolean network.

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

from sys import setrecursionlimit

import random # importing the random module

import argparse
import json
import os
import subprocess
import sys
import time
import tempfile
import xml.etree.ElementTree as etree
from typing import Generator, IO, List, Set

import networkx as nx

from pyeda.boolalg import boolfunc
from pyeda.boolalg.bdd import bddvar, expr2bdd
from pyeda.boolalg.expr import expr

from GraphLLSigned import GraphLLSigned

from networkx.algorithms import bipartite

"""
A python package for approximating minimum feedback vertex sets
"""
from FVSpython3 import FVS as FVS

funs = {}

"""
BDD variables
"""
bdd_vars = {}

"""
BDDs of Boolean functions
"""
bdd_funs = {}

"""
Negative feedback vertex set
"""
U_neg = []

"""
Petri net encoding of the ABN
"""
petri_net = nx.DiGraph()

"""
List of source nodes
"""

source_nodes = []

"""
Node to input nodes
"""

INx = {}

version = "0.0.0"

def add_edges(net: nx.DiGraph, tname: str, things: boolfunc, source: str):
    """Add all edges from things to tname and back in net except for source."""
    if source.startswith("-"):
        nsource = source[1:]
    else:
        nsource = "-" + source

    for i, t in enumerate(things.satisfy_all()):
        name = f"{tname}_{i}"
        net.add_node(name, kind="transition")
        for p, v in t.items():
            if v == 0:
                pname = "-" + str(p)
            else:
                pname = str(p)
            net.add_edge(pname, name)
            if pname == source:
                net.add_edge(name, nsource)
            else:
                net.add_edge(name, pname)

def read_network_structure(fileobj: IO):
    """Parse a BoolNet .bnet file and get static information."""

    setrecursionlimit(2048)
    
    for line in fileobj.readlines():
        if line.startswith("#") or line.startswith("targets,"):
            continue
        try:
            x, fx = line.replace(" ", "").replace("-", "_").replace("!", "~").split(",", maxsplit=1)
        except ValueError:  # not enough values to unpack
            continue
        
        x = x.strip()
        
        petri_net.add_node(x, kind="place")
        petri_net.add_node(
            "-" + x, kind="place"
        )

        if fx.strip() == x:
            source_nodes.append(x)

        vx = bddvar(x)
        fx = expr(fx) # Boolean function in form of pyeda.boolalg.expr
        INx[x] = list(fx.support) # list of nodes appearing in Boolean function fx

        funs[x] = fx

        fx = expr2bdd(expr(fx)) # Boolean function in form of pyeda.boolalg.bdd
        bdd_funs[x] = fx
        bdd_vars[x] = vx

        activate = fx & ~vx
        inactivate = ~fx & vx

        add_edges(petri_net, f"tp_{x}", activate, "-" + x)
        add_edges(petri_net, f"tn_{x}", inactivate, x)
    

def find_minimum_NFVS():
    nodes = bdd_funs.keys()
            
    """Build the unsigned and signed interaction graphs"""
    u_ig = nx.DiGraph()

    i_node = 1
    vertex_list = []
    node2id = {}
    id2node = {}

    for node in nodes:
        vertex_list.append(i_node)

        node2id[node] = i_node
        id2node[i_node] = node

        i_node += 1

    s_ig = GraphLLSigned(vertex_list)

    for x in nodes:
        u_ig.add_node(x)

        fx = bdd_funs[x]

        for y in INx[x]:
            is_actual_arc = False

            vy = bdd_vars[str(y)]
            
            fx_res_vy_0 = fx.restrict({vy: 0})
            fx_res_vy_1 = fx.restrict({vy: 1})

            pos_arc = ~fx_res_vy_0 & fx_res_vy_1
            neg_arc = fx_res_vy_0 & ~fx_res_vy_1

            y_id = node2id[str(y)]
            x_id = node2id[str(x)]

            if pos_arc.is_one() or pos_arc.satisfy_one():
                # a positive arc with weight = 1
                s_ig.setEdge(y_id, x_id, 1)

                is_actual_arc = True

            if neg_arc.is_one() or neg_arc.satisfy_one():
                # a negative arc with weight = -1
                s_ig.setEdge(y_id, x_id, -1)
                is_actual_arc = True

            if is_actual_arc == True:
                u_ig.add_edge(str(y), str(x))
                


    """Find feedback vertex set"""
    U = FVS.FVS(u_ig)

    U = list(set(U) - set(source_nodes))

    # Compute a negative feedback vertex set
    U_neg_id = s_ig.getSelfNegativeLoops()
    U_candidate = []

    for v in U:
        v_id = node2id[v]
        if not v_id in U_neg_id:
            U_candidate.append(v_id)

    for v in U_neg_id:
        s_ig.removeVertex(v)

    for v in source_nodes:
        v_id = node2id[v]

        s_ig.removeVertex(v_id)
    
    while not IsNoNegativeCycle(s_ig):
        v_id = SelectByDegreeNegative(s_ig, U_candidate)

        if v_id == -1:
            break
    
        U_candidate.remove(v_id)

        U_neg_id.append(v_id)
        
        s_ig.removeVertex(v_id)

    result = []
    for v_id in U_neg_id:
        result.append(id2node[v_id])
    
    return result


def IsNoNegativeCycle(s_ig: GraphLLSigned) -> bool:
    udGraph = s_ig.convertToUDGraph()
    return bipartite.is_bipartite(udGraph)


def SelectByDegreeNegative(s_ig: GraphLLSigned, U_candidate: list[int]) -> int:
    v_selected = -1
    maxNegDeg = -1

    for v_id in U_candidate:
        v_neg_deg = s_ig.GetDegreeNegative(v_id)

        if v_neg_deg >= maxNegDeg:
            v_selected = v_id
            maxNegDeg = v_neg_deg

    return v_selected


def pnml_to_asp(name: str) -> str:
    """Convert a PNML id to an ASP variable."""
    if name.startswith("-"):
        return "n" + name[1:]
    return "p" + name


def write_asp(petri_net: nx.DiGraph, asp_file: IO):
    """Write the ASP program for the maximal conflict-free siphons of petri_net."""
    for node, kind in petri_net.nodes(data="kind"):
        if kind == "place":
            print("{", pnml_to_asp(node), "}.", file=asp_file, sep="")
            if not node.startswith("-"):
                print(
                    f":- {pnml_to_asp(node)}, {pnml_to_asp('-' + node)}.", file=asp_file
                )  # conflict-freeness
        else:  # it's a transition, apply siphon (if one succ is true, one pred must be true)
            preds = list(petri_net.predecessors(node))
            or_preds = "; ".join(map(pnml_to_asp, preds))
            for succ in petri_net.successors(node):
                if succ not in preds:  # optimize obvious tautologies
                    print(f"{or_preds} :- {pnml_to_asp(succ)}.", file=asp_file)


def write_asp_fix(petri_net: nx.DiGraph, nodes: List[str], retain_set: dict, asp_file: IO):
    """Write the ASP program for deadlocks of petri_net."""
    for node in nodes:
        pX = "p" + node
        nX = "n" + node

        print(
            "{", pX, "}."
            , file=asp_file, sep=""
        )

        print(
            "{", nX, "}."
            , file=asp_file, sep=""
        )


        atom_lhs = pX + "; " + nX
        print(
            "1 {", atom_lhs, "} 1."
            , file=asp_file, sep=""
        )
        
    for node, kind in petri_net.nodes(data="kind"):
        if kind == "place":
            continue
        else:  # it's a transition
            preds = list(petri_net.predecessors(node))
            atoms = []

            for pred in preds:
                atoms.append(pnml_to_asp(pred))

            pred_rhs = "; ".join(atoms)
            print(
                f":- {pred_rhs}."
                , file=asp_file, sep=""
            )


def solve_asp(asp_filename: str, max_output: int, time_limit: int) -> str:
    """Run an ASP solver on program asp_file and get the solutions."""
    result = subprocess.run(
        [
            "clingo",
            str(max_output),
            "--heuristic=Domain",  # maximal w.r.t. inclusion
            "--enum-mod=domRec",
            "--dom-mod=3",
            "--outf=2",  # json output
            f"--time-limit={time_limit}",
            asp_filename,
        ],
        capture_output=True,
        text=True,
    )

    # https://www.mat.unical.it/aspcomp2013/files/aspoutput.txt
    # 30: SAT, all enumerated, optima found, 10 stopped by max
    if result.returncode != 30 and result.returncode != 10:
        print(f"Return code from clingo: {result.returncode}")
        result.check_returncode()  # will raise CalledProcessError

    return result.stdout


def solution_to_bool(places: List[str], sol: List[str]) -> List[str]:
    """Convert a list of present places in sol, to a tri-valued vector."""
    return [place_in_sol(sol, p) for p in places]


def solution_to_bool_fix(places: List[str], sol: List[str]) -> List[str]:
    """Convert a list of present places in sol, to a bi-valued vector."""
    return [place_in_sol_fix(sol, p) for p in places]


def place_in_sol(sol: List[str], place: str) -> str:
    """Return 0/1/- if place is absent, present or does not appear in sol.

    Remember that being in the siphon means staying empty, so the opposite value is the one fixed.
    """
    if "p" + place in sol:
        return "0"
    if "n" + place in sol:
        return "1"
    return "-"


def place_in_sol_fix(sol: List[str], place: str) -> str:
    """Return 0/1/- if place is absent, present sol."""
    if "p" + place in sol:
        return "1"
    if "n" + place in sol:
        return "0"
    return "0"


def get_solutions(
    asp_output: str, places: List[str]
) -> Generator[List[str], None, None]:
    """Display the ASP output back as trap spaces."""
    solutions = json.loads(asp_output)
    yield from (
        solution_to_bool(places, sol["Value"])
        for sol in solutions["Call"][0]["Witnesses"]
    )


def get_solutions_fix(
    asp_output: str, places: List[str]
) -> Generator[List[str], None, None]:
    """Display the ASP output back as fixed points."""
    solutions = json.loads(asp_output)
    yield from (
        solution_to_bool_fix(places, sol["Value"])
        for sol in solutions["Call"][0]["Witnesses"]
    )


def get_asp_output(
    petri_net: nx.DiGraph, max_output: int, time_limit: int
) -> str:
    """Generate and solve ASP file."""
    (fd, tmpname) = tempfile.mkstemp(suffix=".lp", text=True)
    with open(tmpname, "wt") as asp_file:
        write_asp(petri_net, asp_file)
    solutions = solve_asp(tmpname, max_output, time_limit)
    os.close(fd)
    os.unlink(tmpname)
    return solutions

def get_asp_output_fix(
    petri_net: nx.DiGraph, nodes: List[str], retain_set: dict, max_output: int, time_limit: int
) -> str:
    """Generate and solve ASP file."""
    (fd, tmpname) = tempfile.mkstemp(suffix=".lp", text=True)
    with open(tmpname, "wt") as asp_file:
        write_asp_fix(petri_net, nodes, retain_set, asp_file)
    solutions = solve_asp(tmpname, max_output, time_limit)
    os.close(fd)
    os.unlink(tmpname)
    return solutions


def compute_trap_spaces(
    petri_net: nx.DiGraph,
    nodes: List[str],
    display: bool = False,
    max_output: int = 0,
    time_limit: int = 0,
):
    """Do the minimal trap-space computation."""

    solutions_output = get_asp_output(petri_net, max_output, time_limit)
    solutions = get_solutions(solutions_output, nodes)

    result = []
    for solution in solutions:
        space = {}
        for (node, value) in zip(nodes, solution):
            if value == "0":
                space[node] = "0"
            if value == "1":
                space[node] = "1"
            if value == "-":
                space[node] = "-"
            
        result.append(space)
    
    return result
    
def compute_fixed_points_reduced_STG(
    petri_net: nx.DiGraph,
    nodes: List[str],
    retained_set: dict,
    display: bool = False,
    max_output: int = 0,
    time_limit: int = 0,
):
    """Do the fixed point computation of the reduced STG."""

    reduced_petri_net = petri_net.copy()
    for node in retained_set.keys():
        b_i = retained_set[node]
        source_place = ""

        if b_i == 0:
            source_place = "-" + node

        if b_i == 1:
            source_place = node

        preds = list(reduced_petri_net.predecessors(source_place))
        succs = list(reduced_petri_net.successors(source_place))

        deleted_transitions = list(set(succs) - set(preds))

        for trans in deleted_transitions:
            reduced_petri_net.remove_node(trans)

    solutions_output = get_asp_output_fix(reduced_petri_net, nodes, retained_set, max_output, time_limit)
    solutions = get_solutions_fix(solutions_output, nodes)

    result = []
    for solution in solutions:
        space = {}
        for (place,value) in zip(nodes, solution):
            if value == "0":
                space[place] = "0"
            if value == "1":
                space[place] = "1"
            if value == "-":
                space[place] = "-"
            
        result.append(space)
    
    return result


def get_retained_set(U_neg: List[str]):
    retained_set = {}

    for node in U_neg:
        f_i = funs[node]
        n_input = len(INx[node])
        n_poss_sat = pow(2, n_input - 1)

        n_sat = f_i.satisfy_count()
        
        if n_sat > n_poss_sat:
            retained_set[node] = 1
        elif n_sat < n_poss_sat:
            retained_set[node] = 0
        else:
            retained_set[node] = random.randint(0, 1)
        
    return retained_set


def compute_attractors(
    infile: IO,
    mts_file: IO,
    std_file: IO,
    result_file:IO,
    display: bool = False,
    max_output: int = 0,
    time_limit: int = 0,
):
    """Do the attractor computation on input file infile."""
    toclose = False
    if isinstance(infile, str):
        infile = open(infile, "r", encoding="utf-8")
        toclose = True

    if infile.name.endswith(".bnet"):
        read_network_structure(infile)
    else:
        infile.close()
        raise ValueError("Currently limited to parsing .bnet files")

    if toclose:
        infile.close()


    U_neg = find_minimum_NFVS()

    retained_set = get_retained_set(U_neg)

    nodes = bdd_funs.keys()

    M = compute_trap_spaces(petri_net, nodes, max_output=0)
    
    write_file_time = 0
    start = time.process_time()

    for node in nodes:
        print(
            f"{node},", file=mts_file
        )

    n_mts = 0
    for m in M:
        n_mts += 1
        mts = ""

        for node in nodes:
            mts += m[node]

        print(
            f"min trap space {n_mts} : {mts}", file=mts_file
        )

    write_file_time += time.process_time() - start

    F = compute_fixed_points_reduced_STG(petri_net, nodes, retained_set, max_output=0)

    start = time.process_time()
    for node in nodes:
        print(
            f"{node},", file=std_file
        )

    n_cand = 0
    for s in F:
        n_cand += 1
        std = ""

        for node in nodes:
            std += s[node]

        print(
            f"steady state {n_cand} : {std}", file=std_file
        )

    write_file_time += time.process_time() - start
    return write_file_time

