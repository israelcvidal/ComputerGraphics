class Material(object):
    def __init__(self, k_a_rgb, k_d_rgb, k_e_rgb):
        self.k_a_rgb = k_a_rgb
        self.k_d_rgb = k_d_rgb
        self.k_e_rgb = k_e_rgb


class Face(object):
    def __init__(self, face_id, vertices, material, normal):
        self.vertices = vertices
        self.face_id = face_id
        self.material = material
        self.normal = normal


class Obj(object):
    def __init__(self):
        self.vertex_id = 0
        self.face_id = 0
        self.vertices = {}
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
        self.vertices[id_] = [x, y, z]
        self.vertex_id += 1
        return id_

    def add_face(self, e1, e2, e3, material):
        """
        Creates a new face(adding do self.faces dictionary) composed by edges e1, e2 and e3

        :param e1: edge 1 id
        :param e2: edge 2 id
        :param e3: edge 3 id
        :return: face's id
        """
        id_ = self.face_id
        normal = (e3-e1).cross(e2-e1)

        face = Face(id_, [e1, e2, e3], material, normal)
        self.faces[id_] = face
        self.face_id += 1
        return id_


