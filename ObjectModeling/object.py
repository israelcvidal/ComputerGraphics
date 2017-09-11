class Obj(object):
    def __init__(self):
        self.vertex_id = 0
        self.edge_id = 0
        self.face_id = 0
        self.vertices = {}
        self.edges = {}
        self.faces = {}

    def add_vertex(self, x, y, z):
        """
        Creates a new vertex with a sequential id and makes its coordinates be x, y, z
        Finally add this vertex do self.vertices dictionary.
        Return new vertex' id

        :param x: coordinate x
        :param y: coordinate y
        :param z: coordinate z
        :return: vertex's id
        """
        id_ = self.vertex_id
        self.vertices[id] = [x, y, z]
        self.vertex_id += 1
        return id_

    def add_edge(self, v1, v2):
        """
        Creates a new edge(adding to self.edges dictionary) from v1 to v2 and then returns edge's id

        :param v1: vertex 1 id
        :param v2: vertex 2 id
        :return: edge's if
        """
        id_ = self.edge_id
        self.edges[id_] = [v1, v2]
        self.edge_id += 1
        return id_

    def add_face(self, e1, e2, e3):
        """
        Creates a new face(adding do self.faces dictionary) composed by edges e1, e2 and e3

        :param e1: edge 1 id
        :param e2: edge 2 id
        :param e3: edge 3 id
        :return: face's id
        """

        id_ = self.face_id
        self.face_id = [e1, e2, e3]
        self.face_id += 1
        return id_

class Cube(Obj):
    def __init__(self):
        super.__init__()
        # Creating vertices
        v0 = self.add_vertex(0, 0, 0)
        v1 = self.add_vertex(1, 0, 0)
        v2 = self.add_vertex(0, 1, 0)
        v3 = self.add_vertex(1, 1, 0)
        v4 = self.add_vertex(0, 0, 1)
        v5 = self.add_vertex(1, 0, 1)
        v6 = self.add_vertex(0, 1, 1)
        v7 = self.add_vertex(1, 1, 1)

        # Creating edges
        e0 = self.add_edge(v0, v1)
        e1 = self.add_edge(v0, v2)
        e2 = self.add_edge(v0, v3)
        e3 = self.add_edge(v2, v3)
        e4 = self.add_edge(v3, v1)
        e5 = self.add_edge(v4, v5)
        e6 = self.add_edge(v4, v6)
        e7 = self.add_edge(v4, v7)
        e8 = self.add_edge(v6, v7)
        e9 = self.add_edge(v7, v5)
        e10 = self.add_edge(v0, v4)
        e11 = self.add_edge(v2, v6)
        e12 = self.add_edge(v0, v6)
        e13 = self.add_edge(v1, v5)
        e14 = self.add_edge(v3, v7)
        e15 = self.add_edge(v1, v7)
        e16 = self.add_edge(v3, v6)
        e17 = self.add_edge(v1, v4)

        # Creating faces

        f0 = self.add_face(e2, e4, e0)
        f1 = self.add_face(e1, e3, e2)
        f2 = self.add_face(e9, e13, e15)
        f3 = self.add_face(e15, e4, e14)
        f4 = self.add_face(e5, e9, e7)
        f5 = self.add_face(e7, e8, e6)
        f6 = self.add_face(e12, e10, e6)
        f7 = self.add_face(e11, e1, e12)
        f8 = self.add_face(e17, e13, e5)
        f9 = self.add_face(e10, e0, e17)
        f10 = self.add_face(e8, e14, e16)
        f11 = self.add_face(e16, e3, e11)

if __name__ == '__main__':
    cube = Obj()
