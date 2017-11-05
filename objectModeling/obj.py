import numpy as np


class Material(object):
    def __init__(self, k_a_rgb, k_d_rgb, k_e_rgb, attenuation):
        self.k_a_rgb = k_a_rgb
        self.k_d_rgb = k_d_rgb
        self.k_e_rgb = k_e_rgb
        self.attenuation = attenuation


class Face(object):
    def __init__(self, face_id, vertices, material, normal):
        self.vertices = vertices
        self.face_id = face_id
        self.material = material
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
        self.vertices.append([x, y, z, 1])
        return len(self.vertices)-1

    def add_face(self, p1_id, p2_id, p3_id, material):
        """
        Creates a new face(adding do self.faces dictionary) composed by edges p1, e2 and p3

        :param p1_id: vertex 1 id
        :param p2_id: vertex 2 id
        :param p3_id: vertex 3 id
        :param material: material of the face
        :return: face's id
        """
        p1 = np.array(self.vertices[p1_id])
        p2 = np.array(self.vertices[p2_id])
        p3 = np.array(self.vertices[p3_id])

        id_ = len(self.faces)
        face = Face(id_, {p1_id: p1, p2_id: p2, p3_id: p3}, material, None)
        self.faces.append(face)
        return id_

    def update_faces(self):
        for face in self.faces:
            p1_id, p2_id, p3_id = face.vertices
            p1 = self.vertices[p1_id]
            p2 = self.vertices[p2_id]
            p3 = self.vertices[p3_id]
            normal = np.cross((p3 - p1)[:3], (p2 - p1)[:3])
            normal = normal / np.linalg.norm(normal)
            normal = np.append(normal, [0])
            face.normal = normal
            face.vertices = [p1, p2, p3]

    def get_face(self, face_id):
        return self.faces[face_id]

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]
