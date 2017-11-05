import numpy as np
import math
import sys
sys.path.append("..")
from transformations import world_camera_transformations as wct
from objectModeling import obj
import matplotlib.pyplot as plt


class Scenario(object):
    def __init__(self, objects=[], light_sources=[], po=None, look_at=None,
                 a_vup=None, background_color=[0.0, 0.0, 0.0], ambient_light=[1.0, 1.0, 1.0]):
        """

        :param objects: list of all objects on the scenario
        :param light_sources: list of all light sources on the scenario
        :param po: observer(camera) location on world coordination
        :param look_at: loot at point
        :param a_vup: view up point
        """
        self.objects = objects
        self.light_sources = light_sources
        self.po = po
        self.look_at = look_at
        self.a_vup = a_vup
        self.background_color = background_color
        self.ambient_light = np.array(ambient_light)

    def ray_casting(self, window_width, window_height, window_distance, pixels_width, pixels_height):
        """

        :param window_width: width of window to open on the plane
        :param window_height: height of window to open on the plane
        :param window_distance: distance of the plane where the window will be opened at
        :param pixels_width: number of pixels we will have on width direction
        :param pixels_height: number of pixels we will have on height direction
        :return: matrix rgb to be rendered
        """
        delta_x = window_width / pixels_width
        delta_y = window_height / pixels_height
        # p = matrix of points corresponding to each pixel
        p = np.ones((pixels_width, pixels_height, 3))

        # transforming all objects to camera
        self.transform_to_camera()

        for i in range(pixels_height):
            y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
            for j in range(pixels_width):

                x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)

                pij = np.array([x_i, y_i, -window_distance])

                # getting face  intercepted and point of intersection of ray pij
                objects_not_cut = self.objects_culling(pij)
                faces_to_check_intersection = self.back_face_culling(objects_not_cut, pij)
                p_int, intersected_face = self.get_intersected_face(faces_to_check_intersection, pij)
                # if intercept any point
                if type(p_int).__module__ == np.__name__:
                    # TODO
                    # CHECK IF IT MAKES SENSE
                    p[i][j] = self.determine_color(p_int, intersected_face)
                else:
                    p[i][j] = self.background_color
        return p

    def determine_color(self, p_int, intersected_face):
        """
        Return the RGB color for the pixel ij
        :param p_int: point intersected
        :param intersected_face: face intersected by the ray
        :return:
        """
        pij_rgb = intersected_face.material.k_a_rgb * self.ambient_light
        for light_source in self.light_sources:
            pij_rgb += light_source.get_total_intensity(intersected_face, p_int)

        return pij_rgb

    def objects_culling(self, pij):
        """
        Return objects that the ray intersects with their have intersection sphere(aura)
        :param pij: point corresponding to a pixel ij
        :return:
        """

        objects_not_cut = []

        for object_ in self.objects:
            vertices = np.array(list(object_.vertices.values()))
            min_x = min(vertices[:, 0])
            max_x = max(vertices[:, 0])
            min_y = min(vertices[:, 1])
            max_y = max(vertices[:, 1])
            min_z = min(vertices[:, 2])
            max_z = max(vertices[:, 2])

            center = np.array([(max_x - min_x), (max_y - min_y), (max_z - min_z)])
            radius = math.pow((max_x - center[0]), 2) + math.pow((max_y - center[1]), 2) + math.pow((max_z - center[2]),
                                                                                                    2)
            radius = math.sqrt(radius)
            a = pij.dot(pij)
            b = -2 * (pij.dot(center))
            c = center.dot(center) - math.pow(radius, 2)
            if (math.pow(b, 2) - 4 * a * c) >= 0:
                objects_not_cut.append(object_)

        return objects_not_cut

    def back_face_culling(self, objects, pij):
        """
        Return list of faces from objects that might have intersection with the ray
        :param objects:
        :param pij:
        :return:
        """
        faces_not_cut = []

        pij_u = pij / np.linalg.norm(pij)
        pij_u = np.append(pij_u, [1])
        for object_ in objects:
            for face in object_.faces.values():
                if pij_u.dot(face.normal) < 0:
                    faces_not_cut.append(face)

        return faces_not_cut

    def get_intersected_face(self, faces, pij):
        """
        Returns witch faces have intersection with the ray and their point of intersection(t).
        :param faces: list of faces
        :param pij: point where the ray starts
        :return: point of intersection with the closest face and the face intersected
        """
        intersected_faces = []
        for face in faces:
            p1, p2, p3 = face.vertices.values()
            normal = face.normal[:3]
            p1 = p1[:3]
            p2 = p2[:3]
            p3 = p3[:3]

            t = np.dot(normal, p1[:3]) / np.dot(normal, pij[:3])

            # ray and plane intersection point
            p = t * pij

            # now we want to check if this point is inside the face
            w1 = np.array(p1) - np.array(p)
            w2 = np.array(p2) - np.array(p)
            w3 = np.array(p3) - np.array(p)

            # checking normal of each new triangle
            n1 = np.cross(w1, w2)
            n2 = np.cross(w2, w3)
            n3 = np.cross(w3, w1)

            if n1.dot(n2) >= 0 and n2.dot(n3) >= 0:
                intersected_faces.append((t, face))
        if intersected_faces:
            intersected_faces = sorted(intersected_faces, key=lambda f: f[0])
            intersected_face = None
            for face in intersected_faces:
                if face[0] >= 1:
                    intersected_face = face
                    break
            if intersected_face:
                return intersected_face[0] * pij, intersected_face[1]
        return None, None

    def transform_to_camera(self):
        wc_matrix = wct.get_world_camera_matrix(self.po, self.look_at, self.a_vup)
        for object_ in self.objects:
            camera_vertices = [wc_matrix.dot(vertex) for vertex in object_.vertices.values()]
            for key in object_.vertices.keys():
                object_.vertices[key] = camera_vertices[key]

            object_.update_faces()

        for light_source in self.light_sources:
            if type(light_source) is not InfinityLightSource:
                light_source.position = wc_matrix.dot(light_source.position)

    def transform_to_world(self):
        cw_matrix = wct.get_camera_world_matrix(self.po, self.look_at, self.a_vup)

        for object_ in self.objects:
            world_vertices = [cw_matrix.dot(vertex) for vertex in object_.vertices.values()]
            for key in object_.vertices.keys():
                object_.vertices[key] = world_vertices[key]

            object_.update_faces()

        for light_source in self.light_sources:
            light_source.position = cw_matrix.dot(light_source.position)

    # TODO
    def render(self, window_width, window_height, window_distance, pixels_width, pixels_height):
        scenario = self.ray_casting(window_width, window_height, window_distance, pixels_width, pixels_height)
        plt.imshow(scenario)
        plt.show()


class LightSource(object):
    def __init__(self, intensity, position, direction=None):
        """
        :param intensity: light source intensity, between 0 and 1
        """
        self.intensity = np.array(intensity)
        self.position = np.append(position, [1])
        self.direction = np.array(direction)

    def get_vectors(self, face, p_int):
        """
        Return the unitary vectors n, l, u and r
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n_u = face.normal[:3]

        l = self.position[:3] - p_int
        l_u = (l / np.linalg.norm(l))

        v = -p_int
        v_u = (v / np.linalg.norm(v))

        r = 2 * (np.dot(l_u, n_u)) * n_u - l_u

        return n_u, l_u, v_u, r

    def get_total_intensity(self, face, p_int):
        """
        Return the sum of the diffuse and specular term
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n, l, v, r = self.get_vectors(face, p_int)

        k_d_rgb = face.material.k_d_rgb
        k_e_rgb = face.material.k_e_rgb

        diffuse_term = n.dot(l)
        diffuse_term = max(0, diffuse_term)

        specular_term = np.dot(v, r) ** face.material.attenuation
        specular_term = max(0, specular_term)

        i_obj = (((k_d_rgb * self.intensity) * diffuse_term) +
                 ((k_e_rgb * self.intensity) * specular_term))

        return i_obj


class PunctualLightSource(LightSource):
    def __init__(self, intensity, position):
        """
        :param intensity: light source intensity, between 0 and 1
        :param attenuation: light attenuation for the specular reflection
        :param position: position x,y,z of the light source
        """
        super().__init__(intensity, position, None)


class SpotLightSource(LightSource):
    def __init__(self, intensity, position, direction, theta):
        """
        :param intensity: light source intensity, between 0 and 1
        :param attenuation: light attenuation for the specular reflection
        :param position: position x,y,z of the light source
        :param direction: direction vector of the light
        :param theta: limit angle at which light from source can be seen
        """
        super().__init__(intensity, position, direction)
        self.theta = theta

    def get_total_intensity(self, face, p_int):
        """
        Return the sum of the diffuse and specular term
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n, l, v, r = self.get_vectors(face, p_int)

        k_d_rgb = face.material.k_d_rgb
        k_e_rgb = face.material.k_e_rgb

        spot_intensity = self.direction.dot(-l)
        if spot_intensity < math.cos(self.theta):
            spot_intensity = 0

        diffuse_term = spot_intensity * n.dot(l)
        diffuse_term = max(0, diffuse_term)

        specular_term = spot_intensity * (np.dot(v, r) ** face.material.attenuation)
        specular_term = max(0, specular_term)

        i_obj = (((k_d_rgb * self.intensity) * diffuse_term) +
                 ((k_e_rgb * self.intensity) * specular_term))

        return i_obj


class InfinityLightSource(LightSource):
    def __init__(self, intensity, direction):
        """
        :param intensity: light source intensity, between 0 and 1
        :param attenuation: light attenuation for the specular reflection
        :param direction: direction vector of the light
        """
        super().__init__(intensity=intensity, position=None, direction=direction)

    def get_vectors(self, face, p_int):
        """
        Return the unitary vectors n, l, u and r
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n_u = face.normal[:3]

        l = -self.direction
        l_u = (l / np.linalg.norm(l))

        v = -p_int
        v_u = (v / np.linalg.norm(v))

        r = 2 * (np.dot(l_u, n_u)) * n_u - l_u

        return n_u, l_u, v_u, r
        

def main():
    po = [10, 10, -5, 1.0]
    look_at = [0.5, 0.5, 0.5, 1.0]
    a_vup = [0.5, 3.0, 3.0, 1.0]
    d = 3.
    window_height = 0.5
    window_width = 0.5
    pixels_height = 200
    pixels_width = 200

    red_material = obj.Material([1, 0, 0], [1, 0, 0], [1, 0, 0], 1)
    green_material = obj.Material([0, 1, 0], [0, 1, 0], [0, 1, 0], 1)
    blue_material = obj.Material([0, 0, 1], [0, 0, 1], [0, 0, 1], 1)
    yellow_material = obj.Material([1, 1, 0], [1, 1, 0], [1, 1, 0], 1)
    material = obj.Material([0.3, 0.6, 0.9], [0.3, 0.6, 0.9], [0.3, 0.6, 0.9], 1)
    white_material = obj.Material([1, 1, 1], [1, 1, 1], [1, 1, 1], 1)

    cube = obj.Obj()
    v1 = cube.add_vertex(0.0, 0.0, 0.0)
    v2 = cube.add_vertex(1.0, 0.0, 0.0)
    v3 = cube.add_vertex(0.0, 1.0, 0.0)
    v4 = cube.add_vertex(1.0, 1.0, 0.0)
    v5 = cube.add_vertex(0.0, 0.0, 1.0)
    v6 = cube.add_vertex(1.0, 0.0, 1.0)
    v7 = cube.add_vertex(0.0, 1.0, 1.0)
    v8 = cube.add_vertex(1.0, 1.0, 1.0)
    cube.add_face(v1, v4, v2, red_material)
    cube.add_face(v1, v3, v4, red_material)
    cube.add_face(v2, v8, v6, blue_material)
    cube.add_face(v2, v4, v8, blue_material)
    cube.add_face(v5, v6, v8, green_material)
    cube.add_face(v5, v8, v7, green_material)
    cube.add_face(v1, v5, v7, white_material)
    cube.add_face(v1, v7, v3, white_material)
    cube.add_face(v1, v2, v6, yellow_material)
    cube.add_face(v1, v6, v5, yellow_material)
    cube.add_face(v3, v7, v8, material)
    cube.add_face(v3, v8, v4, material)

    punctual_light = PunctualLightSource([0.7, 0.7, 0.7], [3.5, 3.5, 3.5])
    spot_light = SpotLightSource([0.8, 0.8, 0.8], [0.5, 4.0, 0.5], [5.0, 5.0, 5.0], 10.0)
    infinity_light = InfinityLightSource([0.9, 0.9, 0.9], [10.0, 10.0, 10.0])

    scenario = Scenario([cube], [punctual_light], po, look_at, a_vup)

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()
