import os
import networkx as nx

class GraphLLSigned:
    V: int
    adjacencyListPositive: dict
    adjacencyListNegative: dict
    
    def __init__(self, listVertex: list[int]):
        self.V = len(listVertex)
        self.adjacencyListPositive = {}
        self.adjacencyListNegative = {}
        for node in listVertex:
            self.adjacencyListPositive[node] = []
            self.adjacencyListNegative[node] = []
    

    def convertToUDGraph(self) -> nx.DiGraph:
        vertexCount = -1
        vertexList = []

        udGraph = nx.DiGraph()
        for node in self.adjacencyListPositive.keys():
            vertexList.append(node)
            udGraph.add_node(node)

            if vertexCount < node:
                vertexCount = node

        for node in self.adjacencyListNegative.keys():
            edgeList = self.adjacencyListNegative[node]

            for v in edgeList:
                udGraph.add_edge(node, v)
                udGraph.add_edge(v, node)

        
        for node in self.adjacencyListPositive.keys():
            edgeList = self.adjacencyListPositive[node]

            for v in edgeList:
                if v != node:
                    vertexCount += 1
                    udGraph.add_node(vertexCount)
                    udGraph.add_edge(node, vertexCount)
                    udGraph.add_edge(vertexCount, node)
                    udGraph.add_edge(vertexCount, v)
                    udGraph.add_edge(v, vertexCount)


        return udGraph


    def setEdge(self, y: int, x: int, sign: int):
        if sign == 1:
            self.adjacencyListPositive[y].append(x)
        else:
            self.adjacencyListNegative[y].append(x)


    def isSelfPositiveLoop(self, v: int) -> bool:
        if not self.adjacencyListPositive.has_key(v):
            print("The vertex does not exist")
            return False

        if v in self.adjacencyListPositive[v]:
            return True
        else:
            return False
    

    def isSelfNegativeLoop(self, v: int) -> bool:
        if not self.adjacencyListNegative.has_key(v):
            print("The vertex does not exist")
            return False

        if v in self.adjacencyListNegative[v]:
            return True
        else:
            return False


    def getSelfPositiveLoops(self) -> list[int]:
        result = []

        for node in self.adjacencyListPositive.keys():
            edgeList = self.adjacencyListPositive[node]

            if node in edgeList:
                result.append(node)

        return result
    

    def getSelfNegativeLoops(self) -> list[int]:
        result = []

        for node in self.adjacencyListNegative.keys():
            edgeList = self.adjacencyListNegative[node]

            if node in edgeList:
                result.append(node)

        return result


    def removeVertex(self, v: int):
        # remove vertex v
        del self.adjacencyListPositive[v]
        del self.adjacencyListNegative[v]
        
        self.V = self.V - 1
        
        # update the edge list of each vertex
        for node in self.adjacencyListPositive.keys():
            if v in self.adjacencyListPositive[node]:
                self.adjacencyListPositive[node].remove(v)

        for node in self.adjacencyListNegative.keys():
            if v in self.adjacencyListNegative[node]:
                self.adjacencyListNegative[node].remove(v)


    def GetDegreeNegative(self, v: int) -> int:
        deg_neg = 0

        for node in self.adjacencyListNegative.keys():
            if v == node:
                deg_neg += len(self.adjacencyListNegative[node])
            else:
                if v in self.adjacencyListNegative[node]:
                    deg_neg += 1

        return deg_neg
    
    
