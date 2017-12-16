import numpy as np
#from scipy.spatial.distance import euclidean

class Material(object):
    def __init__(self, k_a_rgb=[1.,1.,1.], k_d_rgb=[1.,1.,1.], k_e_rgb=[1.,1.,1.], attenuation=1.):
        self.k_a_rgb = k_a_rgb
        self.k_d_rgb = k_d_rgb
        self.k_e_rgb = k_e_rgb
        self.attenuation = attenuation


class Vertex(object):
    def __init__(self, vertex_id, coordinates, normal=None):
        self.vertex_id = vertex_id
        self.coordinates = np.array(coordinates)
        self.normal = np.array(normal)


class Face(object):
    def __init__(self, face_id, vertices, material, normal):
        self.vertices = vertices
        self.face_id = face_id
        self.material = material
        self.normal = normal
        self.v0 = None
        self.v1 = None
        self.dot00 = None
        self.dot01 = None
        self.dot11 = None
        self.det = None

    def calculate_normal(self):
        p1, p2, p3 = self.vertices
        normal = np.cross((p2.coordinates - p1.coordinates)[:3], (p3.coordinates - p1.coordinates)[:3])
        normal = normal / np.linalg.norm(normal)
        normal = np.append(normal, [0])
        self.normal = normal

        # calculating dots to optimize barycentric coordinates
        self.v0 = self.vertices[1].coordinates[:3] - self.vertices[0].coordinates[:3]
        self.v1 = self.vertices[2].coordinates[:3] - self.vertices[0].coordinates[:3]

        self.dot00 = np.dot(self.v0, self.v0)
        self.dot01 = np.dot(self.v0, self.v1)
        self.dot11 = np.dot(self.v1, self.v1)
        self.det = self.dot00 * self.dot11 - self.dot01 * self.dot01

    def is_in_triangle(self, p):
        v2 = p - self.vertices[0].coordinates[:3]
        dot02 = np.dot(self.v0, v2)
        dot12 = np.dot(self.v1, v2)

        u = (self.dot11 * dot02 - self.dot01 * dot12) / self.det
        v = (self.dot00 * dot12 - self.dot01 * dot02) / self.det

        w = 1 - u - v

        return 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1


class Obj(object):
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.center = None
        self.radius = None

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
        vertex_id = len(self.vertices)+1
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
        vertices = np.array([vertex.coordinates for vertex in self.vertices])

        self.center = np.mean(vertices, axis=0)
        self.radius = np.max(np.linalg.norm(vertices - self.center, axis=1))

        for face in self.faces:
            face.calculate_normal()

    def apply_transformation(self, M):
        for vertex in self.vertices:
            vertex.coordinates = M.dot(vertex.coordinates)

    def import_obj(self, name, default_mtl=Material()):
        mtl = 'Default'
        materials = {mtl: default_mtl}
        vertices = {}

        with open(name) as file:
            i = 1
            for line in file:
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue

                if values[0] == 'mtllib':
                    materials = self.read_mtllib(values[1])

                if values[0] == 'usemtl':
                    mtl = values[1]

                if values[0] == 'v':
                    vertex = self.add_vertex(float(values[1]), float(values[2]), float(values[3]))
                    vertices[str(vertex.vertex_id)] = vertex
                if values[0] == 'f':
                    self.add_face(vertices[values[1]], vertices[values[2]], vertices[values[3]], materials[mtl])
                if values[0] == 'vn':
                    vertices[str(i)].normal = np.array([float(values[1]), float(values[2]), float(values[3])])
                    i = i + 1

        return self

    def read_mtllib(self, name):
        mtl = None
        materials = {}

        with open(name) as mtllib:
            for line in mtllib:
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue

                if values[0] == 'newmtl':
                    mtl = values[1]
                    materials[mtl] = Material()

                if values[0] == 'Ka':
                    materials[mtl].k_a_rgb = [float(values[1]), float(values[2]), float(values[3])]
                if values[0] == 'Kd':
                    materials[mtl].k_d_rgb = [float(values[1]), float(values[2]), float(values[3])]
                if values[0] == 'Ks':
                    materials[mtl].k_e_rgb = [float(values[1]), float(values[2]), float(values[3])]
                if values[0] == 'Ns':
                    materials[mtl].attenuation = values[1]

        return materials

    def apply_material(self, material):
        for face in self.faces:
            face.material = material

