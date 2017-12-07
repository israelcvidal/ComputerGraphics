import numpy as np
import math
from transformations import world_camera_transformations as wct
import matplotlib.pyplot as plt
import time


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

    def ray_casting(self, window_width, window_height, window_distance, pixels_width, pixels_height, parallel=True):
        """
        :param window_width: width of window to open on the plane
        :param window_height: height of window to open on the plane
        :param window_distance: distance of the plane where the window will be opened at
        :param pixels_width: number of pixels we will have on width direction
        :param pixels_height: number of pixels we will have on height direction
        :return: matrix rgb to be rendered
        """
        print("Starting ray_casting()...")
        start = time.time()

        delta_x = window_width / pixels_width
        delta_y = window_height / pixels_height
        # transforming all objects to camera
        self.transform_to_camera()

        if parallel:
            import pymp
            # p = matrix of points corresponding to each pixel
            p = pymp.shared.array((pixels_width, pixels_height, 3))

            pymp.config.nested = True
            with pymp.Parallel(4) as p1:
                for i in p1.range(pixels_height):
                    y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                    for j in range(pixels_width):
                        x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                        pij = np.array([x_i, y_i, -window_distance])
                        # getting face  intercepted and point of intersection of ray pij
                        objects_not_cut = self.objects_culling(pij)
                        p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                        # if intercept any point
                        if p_int is None:
                            p[i][j] = self.background_color
                        else:
                            p[i][j] = self.determine_color(p_int, intersected_face)
        else:
            # p = matrix of points corresponding to each pixel
            p = np.ones((pixels_width, pixels_height, 3))

            for i in range(pixels_height):
                y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                for j in range(pixels_width):
                    x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                    pij = np.array([x_i, y_i, -window_distance])
                    # getting face  intercepted and point of intersection of ray pij
                    objects_not_cut = self.objects_culling(pij)
                    p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)

                    # if intercept any point
                    if p_int is None:
                        p[i][j] = self.background_color
                    else:
                        p[i][j] = self.determine_color(p_int, intersected_face)
        max_rgb = np.amax(np.amax(p, axis=0), axis=0)

        end = time.time()
        print("Done in: ", end - start)

        return p / [max(1, max_rgb[0]), max(1, max_rgb[1]), max(1, max_rgb[2])]

    def ray_casting_mean(self, window_width, window_height, window_distance, pixels_width, pixels_height, parallel=True):
        """

        :param window_width: width of window to open on the plane
        :param window_height: height of window to open on the plane
        :param window_distance: distance of the plane where the window will be opened at
        :param pixels_width: number of pixels we will have on width direction
        :param pixels_height: number of pixels we will have on height direction
        :return: matrix rgb to be rendered
        """
        print("Starting ray_casting_mean()...")
        start = time.time()

        delta_x = window_width / pixels_width
        delta_y = window_height / pixels_height
        # transforming all objects to camera
        self.transform_to_camera()

        if parallel:
            import pymp
            # p = matrix of points corresponding to each pixel
            p = pymp.shared.array((pixels_height, pixels_width, 3))
            pymp.config.nested = True

            # Borders
            with pymp.Parallel(4) as p1:
                # First and last column:
                for i in p1.range(pixels_height):
                    y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                    for j in [0, pixels_width-1]:
                        x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                        pij = np.array([x_i, y_i, -window_distance])
                        # getting face  intercepted and point of intersection of ray pij
                        objects_not_cut = self.objects_culling(pij)
                        p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                        # if intercept any point
                        if p_int is None:
                            p[i][j] = self.background_color
                        else:
                            p[i][j] = self.determine_color(p_int, intersected_face)

                # First and last line:
                for i in [0, pixels_height-1]:
                    y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                    for j in p1.range(pixels_width):
                        x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                        pij = np.array([x_i, y_i, -window_distance])
                        # getting face  intercepted and point of intersection of ray pij
                        objects_not_cut = self.objects_culling(pij)
                        p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                        # if intercept any point
                        if p_int is None:
                            # print(i, j)
                            p[i][j] = self.background_color
                        else:
                            p[i][j] = self.determine_color(p_int, intersected_face)

                # Alternating pixels
                for i in p1.range(pixels_height):
                    y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                    for j in range(1 + (i % 2), pixels_width, 2):
                        x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                        pij = np.array([x_i, y_i, -window_distance])
                        # getting face  intercepted and point of intersection of ray pij
                        objects_not_cut = self.objects_culling(pij)
                        p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                        # if intercept any point
                        if p_int is None:
                            # print(i, j)
                            p[i][j] = self.background_color
                        else:
                            p[i][j] = self.determine_color(p_int, intersected_face)

            for i in range(0, pixels_height-1):
                for j in range(2 - (i % 2), pixels_width-1, 2):
                    mean1 = (p[i-1][j] + p[i+1][j])/2
                    mean2 = (p[i][j-1] + p[i][j+1])/2
                    diff1 = np.linalg.norm(p[i + 1][j] - p[i - 1][j])
                    diff2 = np.linalg.norm(p[i][j + 1] - p[i][j - 1])
                    if diff1 + diff2 != 0:
                        mean = (mean1*diff2 + mean2*diff1)/(diff1+diff2)
                    else:
                        mean = mean1

                    p[i][j] = mean
        else:
            # p = matrix of points corresponding to each pixel
            p = np.ones((pixels_width, pixels_height, 3))

            # Borders
            # First and last column:
            for i in range(pixels_height):
                y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                for j in [0, pixels_width - 1]:
                    x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                    pij = np.array([x_i, y_i, -window_distance])
                    # getting face  intercepted and point of intersection of ray pij
                    objects_not_cut = self.objects_culling(pij)
                    p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                    # if intercept any point
                    if p_int is None:
                        # print(i, j)
                        p[i][j] = self.background_color
                    else:
                        p[i][j] = self.determine_color(p_int, intersected_face)

            # First and last line:
            for i in [0, pixels_height - 1]:
                y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                for j in range(pixels_width):
                    x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                    pij = np.array([x_i, y_i, -window_distance])
                    # getting face  intercepted and point of intersection of ray pij
                    objects_not_cut = self.objects_culling(pij)
                    p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                    # if intercept any point
                    if p_int is None:
                        # print(i, j)
                        p[i][j] = self.background_color
                    else:
                        p[i][j] = self.determine_color(p_int, intersected_face)

            # Alternating pixels
            for i in range(pixels_height):
                y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
                for j in range(1 + i % 2, pixels_width, 2):
                    x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                    pij = np.array([x_i, y_i, -window_distance])
                    # getting face  intercepted and point of intersection of ray pij
                    objects_not_cut = self.objects_culling(pij)
                    p_int, intersected_face = self.get_intersected_face(objects_not_cut, pij)
                    # if intercept any point
                    if p_int is None:
                        p[i][j] = self.background_color
                    else:
                        p[i][j] = self.determine_color(p_int, intersected_face)

            for i in range(0, pixels_height-1):
                for j in range(2 - (i % 2), pixels_width-1, 2):
                    mean1 = (p[i-1][j] + p[i+1][j])/2
                    mean2 = (p[i][j-1] + p[i][j+1])/2
                    diff1 = np.linalg.norm(p[i + 1][j] - p[i - 1][j])
                    diff2 = np.linalg.norm(p[i][j + 1] - p[i][j - 1])
                    if diff1 + diff2 != 0:
                        mean = (mean1*diff2 + mean2*diff1)/(diff1+diff2)
                    else:
                        mean = mean1
                    p[i][j] = mean

        max_rgb = np.amax(np.amax(p, axis=0), axis=0)

        end = time.time()
        print("Done in: ", end - start)

        return p/[max(1, max_rgb[0]), max(1, max_rgb[1]), max(1, max_rgb[2])]

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
            vertices = np.array([vertex.coordinates for vertex in object_.vertices])
            min_x = min(vertices[:, 0])
            max_x = max(vertices[:, 0])
            min_y = min(vertices[:, 1])
            max_y = max(vertices[:, 1])
            min_z = min(vertices[:, 2])
            max_z = max(vertices[:, 2])

            center = np.array([(max_x + min_x)/2, (max_y + min_y)/2, (max_z + min_z)/2])
            dx = abs(max_x) + abs(min_x)
            dy = abs(max_y) + abs(min_y)
            dz = abs(max_z) + abs(min_z)

            radius = max(dx, dy, dz)/2

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
            for face in object_.faces:
                if pij_u.dot(face.normal) < 0:
                    faces_not_cut.append(face)

        return faces_not_cut

    def get_intersected_face(self, objects, pij):
        """
        Returns witch faces have intersection with the ray and their point of intersection(t).
        :param pij: point where the ray starts
        :return: point of intersection with the closest face and the face intersected
        """
        intersected_face = (float('inf'), None)

        for object_ in objects:
            for face in object_.faces_to_camera:
                p1 = face.vertices[0].coordinates[:3]
                normal = face.normal[:3]

                n_dot_pij = np.dot(normal, pij[:3])

                # backface culling:
                if n_dot_pij >= 0:
                    continue

                t = np.dot(normal, p1[:3]) / n_dot_pij
                if t < 1 or t > intersected_face[0]:
                    continue

                # ray and plane intersection point
                p = t * pij

                # if the distance of this point to the center of the triangle is
                # greater than the max distance of a point in that triangle, than its not a valid intersection

                # if euclidean(p, face.center) > face.max_distance:
                #     continue

                # now we want to check if this point is inside the face
                if face.is_in_triangle(p):
                    intersected_face = (t, face)

        if intersected_face[1] is not None:
            return intersected_face[0] * pij, intersected_face[1]
        return None, None

    def transform_to_camera(self):
        wc_matrix = wct.get_world_camera_matrix(self.po, self.look_at, self.a_vup)
        for object_ in self.objects:
            for vertex in object_.vertices:
                vertex.coordinates = wc_matrix.dot(vertex.coordinates)[:3]
            object_.calculate_normals()

        for light_source in self.light_sources:
            if type(light_source) is not InfinityLightSource:
                light_source.position = wc_matrix.dot(light_source.position)

    def transform_to_world(self):
        cw_matrix = wct.get_camera_world_matrix(self.po, self.look_at, self.a_vup)

        for object_ in self.objects:
            for vertex in object_.vertices:
                vertex.coordinates = cw_matrix.dot(vertex.coordinates)
            object_.calculate_normals()

        for light_source in self.light_sources:
            light_source.position = cw_matrix.dot(light_source.position)

    def render(self, window_width, window_height, window_distance, pixels_width, pixels_height, ray_mean=True):
        if ray_mean:
            scenario = self.ray_casting_mean(window_width, window_height, window_distance, pixels_width, pixels_height)
        else:
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
        if not diffuse_term > 0:
            return 0

        specular_term = np.dot(v, r)
        specular_term = max(0, specular_term ** face.material.attenuation)

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
        if not diffuse_term > 0:
            return 0

        specular_term = spot_intensity * np.dot(v, r)
        specular_term = max(0, specular_term ** face.material.attenuation)

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
