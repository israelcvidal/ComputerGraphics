import numpy as np


class Material(object):
    def __init__(self, k_a_rgb, k_d_rgb, k_e_rgb, attenuation):
        self.k_a_rgb = k_a_rgb
        self.k_d_rgb = k_d_rgb
        self.k_e_rgb = k_e_rgb
        self.attenuation = attenuation


class Vertex(object):
    def __init__(self, vertex_id, coordinates):
        self.vertex_id = vertex_id
        self.coordinates = coordinates


class Face(object):
    def __init__(self, face_id, vertices, material, normal):
        self.vertices = vertices
        self.face_id = face_id
        self.material = material
        self.normal = normal

    def calculate_normal(self):
        p1, p2, p3 = self.vertices
        normal = np.cross((p3.coordinates - p1.coordinates)[:3], (p2.coordinates - p1.coordinates)[:3])
        normal = normal / np.linalg.norm(normal)
        normal = np.append(normal, [0])
        self.normal = normal


class Obj(object):
    def __init__(self):
        self.vertices = []
        self.faces = []

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
        vertex_id = len(self.vertices)
        vertex = Vertex(vertex_id, [x, y, z, 1])
        self.vertices.append(vertex)
        return vertex

    def add_face(self, v1, v2, v3, material):
        """
        Creates a new face(adding do self.faces dictionary) composed by edges p1, e2 and p3

        :param v1: vertex 1
        :param v2: vertex 2
        :param v3: vertex 3
        :param material: material of the face
        :return: face's id
        """
        id_ = len(self.faces)
        face = Face(id_, [v1, v2, v3], material, None)
        self.faces.append(face)
        return face

    def calculate_normals(self):
        for face in self.faces:
            face.calculate_normal()

