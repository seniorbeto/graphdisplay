# -*- coding: utf-8 -*-
import math
from graphdisplay import GraphGUI

class AdjacentVertex:
    """ This class allows us to represent a tuple
    with an adjacent vertex
    and the weight associated (by default None, for non-unweighted graphs)"""
    def __init__(self, vertex: object, weight: int = 1) -> None:
        self.vertex = vertex
        self.weight = weight

    def __str__(self) -> str:
        """ returns the tuple (vertex, weight)"""
        if self.weight is not None:
            return '(' + str(self.vertex) + ',' + str(self.weight) + ')'
        else:
            return str(self.vertex)

class Graph:
    def __init__(self, vertices: list, directed: bool = True) -> None:
        """ We use a dictionary to represent the graph
        the dictionary's keys are the vertices
        The value associated for a given key will be the list of their neighbours.
        Initially, the list of neighbours is empty"""
        self._vertices = {}
        for v in vertices:
            self._vertices[v] = []
        self._directed = directed

    def add_edge(self, start: object, end: object, weight: int = 1) -> None:
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return

        # adds to the end of the list of neighbours for start
        self._vertices[start].append(AdjacentVertex(end, weight))

        if not self._directed:
            # adds to the end of the list of neighbors for end
            self._vertices[end].append(AdjacentVertex(start, weight))

    def contain_edge(self, start: object, end: object) -> int:
        """ checks if the edge (start, end) exits. It does
        not exist return 0, eoc returns its weight or 1 (for unweighted graphs)"""
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return 0
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return 0

        # we search the AdjacentVertex whose v is equal to end
        for adj in self._vertices[start]:
            if adj.vertex == end:
                return adj.weight

        return 0  # does not exist

    def remove_edge(self, start: object, end: object):
        """ removes the edge (start, end)"""
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return

        # we must look for the adjacent AdjacentVertex (neighbour)  whose vertex is end, and then remove it
        for adj in self._vertices[start]:
            if adj.vertex == end:
                self._vertices[start].remove(adj)
        if not self._directed:
            # we must also look for the AdjacentVertex (neighbour)  whose vertex is end, and then remove it
            for adj in self._vertices[end]:
                if adj.vertex == start:
                    self._vertices[end].remove(adj)

    def __str__(self) -> str:
        """ returns a string containing the graph"""
        result = ''
        for v in self._vertices:
            result += '\n'+str(v)+':'
            for adj in self._vertices[v]:
                result += str(adj)+"  "
        return result

    def get_adjacents(self, vertex: object) -> list:
        """ returns a Python list containing the adjacent
        vertices of vertex. The list only contains the vertices"""
        if vertex not in self._vertices.keys():
            print(vertex, ' does not exist!')
            return None
        lst_adjacents = []
        for adj in self._vertices[vertex]:
            lst_adjacents.append(adj.vertex)
        return lst_adjacents

    def get_origins(self, vertex: object) -> list:
        """ returns a Python list containing those vertices that have
        an edge to vertex. The list is formed with objects of AdjacentVertex"""
        if vertex not in self._vertices.keys():
            print(vertex, ' does not exist!')
            return None
        lst_origins = []
        for v in self._vertices:
            for adj in self._vertices[v]:
                if vertex == adj.vertex:
                    lst_origins.append(v)
                    break
        return lst_origins

    def min_distance(self, distances: dict, visited: dict) -> int:
        """ This function is used from dijkstra.
        It returns the vertex (index) whose associated value in
        the dictionary distances is the smallest value. We
        only consider the set of vertices that have not been visited"""
        # Initialize minimum distance for next node
        min_distance = math.inf
        min_vertex = None

        # returns the vertex with minimum distance from the non-visited vertices
        for vertex in self._vertices.keys():
            if distances[vertex] <= min_distance and not visited[vertex]:
                min_distance = distances[vertex]  # update the new smallest
                min_vertex = vertex  # update the index of the smallest

        return min_vertex

    def dijkstra(self, origin: object) -> None:
        visited = {}  # for each vertex (key), the value is a boolean indicating if the vertex has been visited
        previous = {}  # for each vertex (key), the value is the previous node in the minimum path from origin
        distances = {}  # for each vertex (key), the value is minimum distance in the minimum path from origin

        # initialize dictionaries
        for v in self._vertices.keys():
            visited[v] = False
            previous[v] = None
            distances[v] = math.inf

        # The distance from origin to itself is 0
        distances[origin] = 0

        for _ in range(len(self._vertices)):
            # pick the non-visited vertex with minimum distance
            u = self.min_distance(distances, visited)
            visited[u] = True
            # get the adjacent vertices of u
            for adj in self._vertices[u]:
                i = adj.vertex
                w = adj.weight
                # for non-visited vertex, we have to check if its distance is greater than the distance from u
                if not visited[i] and distances[i] > distances[u] + w:
                    # we must update because its distance is greater than the new distance
                    distances[i] = distances[u] + w
                    previous[i] = u

        # Finally, we print the minimum path from origin to the other vertices
        self.print_solution(distances, previous, origin)

        return distances, previous

    def print_solution(self, distances: dict, previous: dict, origin: object):
        """Both Dijkstra and Bellman-Ford algorithms use this function.
        For each vertex, the function is able to rebuild the reverse path from i to origin.
        To do this, the function only needs to read the value associated to the vertex in the dictionary
        previous until to reach a vertex whouse associated value is None (origin)"""
        print("Minimum path from ", origin)

        for i in self._vertices.keys():
            if distances[i] != math.inf:
                # minimum_path is the list which contains the minimum path from origin to i
                minimum_path = []
                prev = previous[i]
                # this loop helps us to build the path
                while prev is not None:
                    minimum_path.insert(0, prev)
                    prev = previous[prev]

                # we append the last vertex, which is i
                minimum_path.append(i)

                # we print the path from v to i and the distance

        print(minimum_path)

    def bellmanford(self, origin: object) -> None:
        """Bellman-Ford algorithm for minimum path"""
        previous = {}
        distances = {}
        for v in self._vertices.keys():
            previous[v] = None
            distances[v] = math.inf
        distances[origin] = 0

        for _ in range(len(self._vertices) - 1):
            for u in self._vertices.keys():
                # get all adjacent vertices of u
                for adj in self._vertices[u]:
                    v = adj.vertex
                    w = adj.weight
                    if distances[v] > distances[u] + w:
                        distances[v] = distances[u] + w
                        previous[v] = u

        # final review to check if there is a solution, or there is a negative cicle (therefore, there is no solution)
        for u in self._vertices.keys():
            for adj in self._vertices[u]:
                v = adj.vertex
                w = adj.weight
                if distances[v] > distances[u] + w:
                    # There is at least a negative cicle.
                    print('There is no solution ', origin)
                    return False

        self.print_solution(distances, previous, origin)
        return distances, previous

    def minimum_path(self, start: object, end: object) -> list:
        """ returns a list containing the path from star to end.
        It also returns the distance of the path. If the path
        does not exist, it returns an empty list and infinito"""
        if start not in self._vertices.keys():
            print(start, ' does not exist!!!')
            return None, None
        if end not in self._vertices.keys():
            print(end, ' does not exist!!!')
            return None, None

        distances, previous = self.dijkstra(start)
        if distances[end] == math.inf:
            return [], math.inf

        result = [end]
        prev = previous[end]
        while prev is not None:
            result.insert(0, prev)
            prev = previous[prev]

        return result, distances[end]


if __name__ == '__main__':

    labels = ['A', 'B', 'C', 'D', 'E']
    g = Graph(labels)

    # Now, we add the edges
    g.add_edge('A', 'C', 12)  # A->(12)C
    g.add_edge('A', 'D', 60)  # A->(60)D
    g.add_edge('B', 'A', 10)  # B->(10)A
    g.add_edge('C', 'B', 20)  # C->(20)B
    g.add_edge('C', 'D', 32)  # C->(32)D
    g.add_edge('E', 'A', 7)   # E->(7)A
    g.add_edge('A', 'E', 50)
    #GraphGUI(g)

    my_gragph = Graph(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'Z', 'N', 'O', 'P', 'Q'])
    my_gragph.add_edge('A', 'B', 4)
    my_gragph.add_edge('B', 'C', 8)
    my_gragph.add_edge('C', 'A', 100)
    my_gragph.add_edge('D', 'E', 7)
    my_gragph.add_edge('E', 'F', 10)
    my_gragph.add_edge('F', 'G', 5)
    my_gragph.add_edge('G', 'Z', 6)
    my_gragph.add_edge('A', 'H', 200)
    my_gragph.add_edge('B', 'I', 3)
    my_gragph.add_edge('C', 'J', 4)
    my_gragph.add_edge('D', 'K', 5)
    my_gragph.add_edge('E', 'L', 6)
    my_gragph.add_edge('F', 'D', 3)
    my_gragph.add_edge('G', 'H', 9)
    my_gragph.add_edge('H', 'Z', 2)
    my_gragph.add_edge('I', 'J', 1)
    my_gragph.add_edge('J', 'A', 6)
    my_gragph.add_edge('K', 'L', 5)
    my_gragph.add_edge('L', 'M', 4)
    my_gragph.add_edge('M', 'H', 3)
    my_gragph.add_edge('N', 'O', 2)
    my_gragph.add_edge('O', 'P', 1)
    my_gragph.add_edge('P', 'Q', 7)
    my_gragph.add_edge('H', 'A', 20)
    my_gragph.add_edge('K', 'B', 7)
    my_gragph.add_edge('B', 'K', 8)

    my_gragph.minimum_path('A', 'Z')

    GraphGUI(my_gragph, 25, 800, 800)
