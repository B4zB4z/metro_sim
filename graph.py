
class Vertex:
    def __init__(self, key):
        self.key = key 
        self.data = None 
        self.edges = [] 
        self.parent = None 
        self.color = 'white'
        self.distance = float("inf")

    def display(self):
        print(self.key, " ", self.data, " ", self.distance, end=": [ ")
        for edge in self.edges:
            print(edge.connection.key, end=" ")
        print("]")


class Edge:
    def __init__(self, vertex):
        self.connection = vertex
        self.weight = 1


class Graph:
    def __init__(self):
        self.vertices = {} 
        self.directed = False
        self.queue = []
        self.start = None

    def display(self): 
        for key in self.vertices:
            self.vertices[key].display()

    def add(self, key):
        if key in self.vertices:
            return None
        else:
            new_vertex = Vertex(key)
            self.vertices[key] = new_vertex
            return new_vertex

    def connect(self, key_a, key_b, **kwargs):
        if key_a not in self.vertices or key_b not in self.vertices:
            return False, "Key not found"
        else:
            weight = 1
            if len(kwargs) > 0 and 'weight' in kwargs:
                weight = kwargs['weight']
            vertex_a = self.vertices[key_a]
            vertex_b = self.vertices[key_b]
            edge = Edge(vertex_b)
            edge.weight = weight
            vertex_a.edges.append(edge)
            if not self.directed:
                edge = Edge(vertex_a)
                edge.weight = weight
                vertex_b.edges.append(edge) 
            return True, "Vertices connected"

    def init_bfs(self):
        for key in self.vertices:
            v = self.vertices[key]
            v.parent = None 
            v.distance = float("inf")
            v.color = 'white'

    def relax(self, va, vb, w):
        if va.distance + w < vb.distance:
            vb.distance = va.distance + w
            vb.parent = va

    def dijkstra(self, start):
        self.start = start
        self.init_bfs()
        if start not in self.vertices:
            return False
        v = self.vertices[start]
        v.distance = 0
        Q = list(self.vertices.values())
        while len(Q) > 0:
            Q.sort(key=lambda v : v.distance)
            mv = Q.pop(0)
            for e in mv.edges:
                self.relax(mv, e.connection, e.weight)
              
    def bfs(self, start):
        self.start = start
        self.init_bfs()
        if start not in self.vertices:
            return False
        # put start in Q, and make distance 0 and parent None, and color gray
        v = self.vertices[start]
        v.distance = 0
        v.color = 'grey'
        self.queue.append(v)
        # while Q is not empty
        while len(self.queue) > 0:
            # pick V from the Q
            v = self.queue.pop(0) 
            # make V black 
            v.color = 'black'
            # for each white edge of V
            for e in v.edges:
                con = e.connection
                # make it gray
                if con.color == 'white':
                    con.color = 'gray'
                    # update distance V.dist + 1
                    con.distance = v.distance + 1
                    # update parent to V
                    con.parent = v 
                    # put in the Q
                    self.queue.append(con)
        return True

    def bfs_shortest_path(self, dest):
        if dest in self.vertices:
            v = self.vertices[dest]
            if v.parent is None:
                print("No path from", v.data)
                return False
            self.print_path(v)
            print()
            return True
        else:
            return False
    
    def print_path(self, vertex):
        if vertex.parent is not None:
            self.print_path(vertex.parent)
        print(vertex.data, end=' ')
