# -*- coding: utf-8 -*-
import math

class AdjacentVertex:
    """This class allows us to represent a tuple with an adjacent vertex
    and the weight associated (by default 1, for non-unweighted graphs)"""

    def __init__(self, vertex, weight=None):
        self._vertex = vertex
        self._weight = weight

    def __str__(self):
        if self._weight != None:
            return '(' + str(self._vertex) + ',' + str(self._weight) + ')'
        else:
            return str(self._vertex)


class Graph():
    def __init__(self, vertices, directed=True):
        """We use a dictionary to represent the graph
        the dictionary's keys are the vertices
        The value associated for a given key will be the list of their neighbours.
        Initially, the list of neighbours is empty"""
        self._vertices = {}
        for v in vertices:
            self._vertices[v] = []
        self._directed = directed

    def addEdge(self, start, end, weight=None):
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return

        # adds to the end of the list of neigbours for start
        self._vertices[start].append(AdjacentVertex(end, weight))

        if self._directed == False:
            # adds to the end of the list of neigbours for end
            self._vertices[end].append(AdjacentVertex(start, weight))

    def containsEdge(self, start, end):
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return 0
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return 0

        # we search the AdjacentVertex whose v is end
        for adj in self._vertices[start]:
            if adj._vertex == end:
                if adj._weight != None:
                    return adj._weight
                else:
                    return 1  # unweighted graphs
        return 0  # does not exist

    def removeEdge(self, start, end):
        if start not in self._vertices.keys():
            print(start, ' does not exist!')
            return
        if end not in self._vertices.keys():
            print(end, ' does not exist!')
            return

        # we must look for the adjacent AdjacentVertex (neighbour)  whose vertex is end, and then remove it
        for adj in self._vertices[start]:
            if adj._vertex == end:
                self._vertices[start].remove(adj)
        if self._directed == False:
            # we must also look for the AdjacentVertex (neighbour)  whose vertex is end, and then remove it
            for adj in self._vertices[end]:
                if adj._vertex == start:
                    self._vertices[end].remove(adj)

    def __str__(self):
        result = ''
        for v in self._vertices:
            result += '\n' + str(v) + ':'
            for adj in self._vertices[v]:
                result += str(adj) + "  "
        return result

    def add_vertex(self, vertex: str) -> None:
        if vertex in self._vertices.keys():
            print(vertex, ' already exists!')
            return
        self._vertices[vertex] = []

    def _dfs(self, vertex: str, visited: dict) -> None:
        visited[vertex] = True
        for adj in self._vertices[vertex]:
            # adj is an object of AdjacentVertex
            adj_vertex = adj.vertex
            if not visited[adj_vertex]:
                self._dfs(adj_vertex, visited)

    def _bfs(self, vertex: str, visited: dict) -> None:
        queue = [vertex]
        visited[vertex] = True
        while len(queue) > 0:
            u = queue.pop(0)
            for adj in self._vertices[u]:
                # remember that adj is an AdjacentVertex
                if not visited[adj.vertex]:
                    queue.append(adj.vertex)
                    visited[adj.vertex] = True

    def non_accessible(self, vertex: str) -> list:
        """gets a vertex and returns the list of vertices
        that cannot be reached from vertex, that is, there is no path
        from vertex to these vertices"""
        # First, we need to obtain all vertices that can be
        # reached from vertex. To do this, we can apply
        # the algorithms of dfs or bfs
        visited = {}
        for v1 in self._vertices:
            visited[v1] = False
        self._dfs(vertex, visited)
        # The function _dfs will visit all vertices reachable
        # from vertex. Therefore, the non-visited vertices
        # will form the list of non-accessible vertices from vertex
        result = []  # list with the non-accessible vertices
        for v1 in self._vertices:
            if not visited[v1]:
                result.append(v1)

        return result

    def get_reachable(self, vertex: str, alg: str = '_dfs') -> list:
        """gets a vertex and returns the list of vertices
        that can be reached from vertex, that is, there is a path
        from vertex to these vertices"""
        # First, we need to obtain all vertices that can be
        # reached from vertex. To do this, we can apply
        # the algorithms of dfs or bfs
        visited = {}
        for v1 in self._vertices:
            visited[v1] = False
        if alg == '_dfs':
            self._dfs(vertex, visited)
        else:
            self._bfs(vertex, visited)

        # The function _dfs will visit all vertices reachable
        # from vertex. Therefore, the visited vertices
        # will form the list of accessible vertices from vertex
        result = []  # list with the accessible vertices
        for v1 in self._vertices:
            if visited[v1]:
                result.append(v1)

        return result

    def _check_bipartite(self, source: str, color: dict) -> bool:

        # Assign first color to source
        queue = [source]
        color[source] = 1
        # similar to bfs
        while len(queue):
            u = queue.pop(0)
            for adj in self._vertices[u]:
                adj_vertex = adj.vertex
                if color[adj_vertex] is None:
                    color[adj_vertex] = 1 - color[u]
                    queue.append(adj_vertex)
                elif color[adj_vertex] == color[u]:
                    return False

        # If we reach here, then all adjacent
        # vertices can be colored with alternate
        # color
        return True

    def check_bipartite(self) -> bool:
        """ returns True if the graph is bipartite and False eoc
        A graph is bipartite is a graph whose vertices can be divided
        into two independent sets, U and V
        such that every edge (u, v) either connects a vertex
        from U to V or a vertex from V to U.
        In other words, for every edge (u, v), either u belongs to U and v to V,
         or u belongs to V and v to U. We can also say that there is no edge
         that connects vertices of same set. """
        color = {}
        # We use a dictionary color to save the color
        # assigned to each vertex: 1 means first color (origins)
        # , 0 means second color (target)
        for v1 in self._vertices:
            color[v1] = None

        for v1 in self._vertices:
            if color[v1] is None:
                if not self._check_bipartite(v1, color):
                    return False

        return True

    def _has_cycles_bfs(self, vertex: str, visited: dict) -> bool:
        """This is function is based on bfs to detect if there is
        some cycle in the breadth traversal from vertex. It uses the dictionary
        visited and the parent of the vertices to detect
        cycle in subgraph reachable from vertex v."""

        # Mark the current vertex as visited
        queue = [vertex]
        parents = {}
        for v1 in self._vertices:
            parents[v1] = None

        while len(queue) > 0:
            s = queue.pop(0)
            visited[s] = True
            for adj in self._vertices[s]:
                adj_vertex = adj.vertex
                if not visited[adj_vertex]:
                    visited[adj_vertex] = True
                    queue.append(adj_vertex)
                    parents[adj_vertex] = s
                elif parents[s] != adj_vertex:
                    # if the ajd_vertex has been already visited,
                    # and it is not the parent of current vertex,
                    # then there is a cycle
                    return True
        return False

    def _has_cycles_dfs(self, vertex: str, visited: dict, parent: str) -> bool:
        """This is recursive function that uses the dictionary
        visited and the parent of the vertices to detect
        cycle in subgraph reachable from vertex v."""

        # Mark the current vertex as visited
        visited[vertex] = True
        # Recur for all the vertices
        # adjacent to this vertex
        for adj in self._vertices[vertex]:
            adj_vertex = adj.vertex
            # If the node is not visited then recurse on it
            if not visited[adj_vertex]:
                if self._has_cycles_dfs(adj_vertex, visited, vertex):
                    return True
            elif parent != adj_vertex:
                # if the ajd_vertex has been already visited,
                # and it is not the parent of current vertex,
                # then there is a cycle
                return True
        print()
        return False

    def _has_cycles_directed(self, vertex: str, visited: dict, rec_stack: dict) -> bool:
        """detects a cycle in a directed graph using the
        dfs alg. Moreover, visited and rec_stack allow us
        to detect if a vertex has been previously visited."""

        # Mark the current vertex as visited
        visited[vertex] = True
        rec_stack[vertex] = True
        # Recur for all the vertices
        # adjacent to this vertex
        for adj in self._vertices[vertex]:
            adj_vertex = adj.vertex
            # If the node is not visited then recurse on it
            if not visited[adj_vertex]:
                if self._has_cycles_directed(adj_vertex, visited, rec_stack):
                    return True
            elif rec_stack[adj_vertex]:
                return True
        # The node needs to be popped from
        # recursion stack before function ends
        rec_stack[vertex] = False
        return False

    def has_cycles(self, alg: str = 'dfs') -> bool:
        """returns True if the graph contains a cycle, False eoc"""
        print(self._directed)
        visited = {}
        recursion_stack = {}

        for v1 in self._vertices:
            visited[v1] = False
            # we will only use it for directed graphs
            recursion_stack[v1] = False

        # Call the recursive helper
        # function to detect cycle in different
        # DFS trees
        for v1 in self._vertices:
            if not visited[v1]:
                if self._directed:
                    result = self._has_cycles_directed(v1, visited, recursion_stack)
                else:
                    if alg == 'dfs':
                        result = self._has_cycles_dfs(v1, visited, None)
                    else:
                        result = self._has_cycles_bfs(v1, visited)

                if result:
                    return True

        return False

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
                i = adj._vertex
                w = adj._weight
                # for non-visited vertex, we have to check if its distance is greater than the distance from u
                if not visited[i] and distances[i] > distances[u] + w:
                    # we must update because its distance is greater than the new distance
                    distances[i] = distances[u] + w
                    previous[i] = u

        # Finally, we print the minimum path from origin to the other vertices
        #self.print_solution(distances, previous, origin)

        return distances, previous

    def print_solution(self, distances: dict, previous: dict, origin: object):
        """Both Dijkstra and Bellman-Ford algorithms use this function.
        For each vertex, the function is able to rebuild the reverse path from i to origin.
        To do this, the function only needs to read the value associated to the vertex in the dictionary
        previous until to reach a vertex whouse associated value is None (origin)"""
        print("Minimum path from ", origin)

        for i in self._vertices.keys():
            if distances[i] == math.inf:
                print("There is not path from ", origin, ' to ', i)
            else:
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
                print(origin, '->', i, ":", minimum_path, distances[i])

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
                v = adj._vertex
                w = adj._weight
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
