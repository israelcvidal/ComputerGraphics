import math
import time
import matplotlib.pyplot as plt
import numpy as np

from ray_casting.transformations import world_camera_transformations as wct


class Window(object):
    def __init__(self, width, height, distance, pixels_width, pixels_height):
        self.width = width
        self.height = height
        self.distance = distance
        self.pixels_width = pixels_width
        self.pixels_height = pixels_height
        self.delta_x = width / pixels_width
        self.delta_y = height / pixels_height

    def get_pij(self, i, j):
        y_i = (self.height - self.delta_y) / 2 - (i * self.delta_y)
        x_i = (-self.width + self.delta_x) / 2 + (j * self.delta_x)
        return np.array([x_i, y_i, -self.distance])


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

    def render(self, window, ray_mean=True, parallel=True, shadow=False, projection_type="PERSPECTIVE",
               oblique_angle=None, oblique_factor=None):

        params = {'parallel': parallel, 'shadow': shadow, 'projection_type': projection_type,
                  'oblique_angle': oblique_angle, 'oblique_factor': oblique_factor}

        scenario = self.ray_casting_mean(window, **params) if ray_mean else self.ray_casting(window, **params)

        plt.imshow(scenario)
        plt.show()

    def get_oblique_options(self, projection_type, oblique_factor):
        projections = {
            'PERSPECTIVE': (False, oblique_factor),
            'CABINET': (True, .5),
            'CAVALIER': (True, 1.),
            'OBLIQUE': (True, oblique_factor),
            'ORTHOGRAPHIC': (True, 0.)
        }
        if projection_type not in projections:
            print("INVALID PROJECTION!")
            exit()
        else:
            return projections[projection_type]

    def ray_casting(self, window, parallel=True, shadow=False, projection_type="CABINET", oblique_angle=0.0, oblique_factor=0.0):

        """
        :param window: object containing width, height, and distance of window to open on the plane.
                Contains also number of pixels in w and h.
        :param parallel: if true, run loop in parallel
        :param shadow: if true, render ray casting with shadow
        :param projection_type: choose between PERSPECTIVE, OBLIQUE, CAVALIER OR CABINET
        :param oblique_angle: angle of projection oblique
        :param oblique_factor: size of projection compared to real object
        :return: matrix rgb to be rendered
        """

        print("Starting ray_casting()...")
        start = time.time()

        self.transform_to_camera()

        oblique, oblique_factor = self.get_oblique_options(projection_type, oblique_factor)

        if parallel:
            import pymp
            pymp.config.nested = True
            p = pymp.shared.array((window.pixels_width, window.pixels_height, 3))

            with pymp.Parallel(4) as p1:
                for i in p1.range(window.pixels_height):
                    for j in range(window.pixels_width):
                        p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor,
                                                          oblique_angle)
        else:
            p = np.ones((window.pixels_width, window.pixels_height, 3))
            for i in range(window.pixels_height):
                for j in range(window.pixels_width):
                    p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor,
                                                      oblique_angle)

        max_rgb = np.amax(np.amax(p, axis=0), axis=0)

        end = time.time()
        print("Done in: ", end - start)

        return p / [max(1, max_rgb[0]), max(1, max_rgb[1]), max(1, max_rgb[2])]

    def ray_casting_mean(self, window, parallel=True, shadow=False, projection_type="CABINET", oblique_angle=45.0, oblique_factor=1.0):
        """
        :param window: object containing width, height, and distance of window to open on the plane.
                Contains also number of pixels in w and h.
        :param parallel: if true, run loop in parallel
        :param shadow: if true, render ray casting with shadow
        :param projection_type: choose between PERSPECTIVE, OBLIQUE, CAVALIER OR CABINET
        :param oblique_angle: angle of projection oblique
        :param oblique_factor: size of projection compared to real object
        :return: matrix rgb to be rendered
        """

        print("Starting ray_casting_mean()...")
        start = time.time()

        self.transform_to_camera()

        oblique, oblique_factor = self.get_oblique_options(projection_type, oblique_factor)

        if parallel:
            import pymp
            pymp.config.nested = True
            p = pymp.shared.array((window.pixels_width, window.pixels_height, 3))

            with pymp.Parallel(4) as p1:

                # First and last column:
                for i in p1.range(window.pixels_height):
                    for j in [0, window.pixels_width - 1]:
                        p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor,
                                                          oblique_angle)

                # First and last line:
                for i in [0, window.pixels_height - 1]:
                    for j in p1.range(window.pixels_width):
                        p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor,
                                                          oblique_angle)

                # Alternating pixels
                for i in p1.range(window.pixels_height):
                    for j in range(1 + (i % 2), window.pixels_width, 2):
                        p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor,
                                                          oblique_angle)

                for i in range(0, window.pixels_height - 1):
                    for j in range(2 - (i % 2), window.pixels_width - 1, 2):
                        mean1 = (p[i - 1][j] + p[i + 1][j]) / 2
                        mean2 = (p[i][j - 1] + p[i][j + 1]) / 2
                        diff1 = np.linalg.norm(p[i + 1][j] - p[i - 1][j])
                        diff2 = np.linalg.norm(p[i][j + 1] - p[i][j - 1])
                        if diff1 + diff2 != 0:
                            mean = (mean1 * diff2 + mean2 * diff1) / (diff1 + diff2)
                        else:
                            mean = mean1

                        p[i][j] = mean
        else:
            p = np.ones((window.pixels_width, window.pixels_height, 3))

            # First and last column:
            for i in range(window.pixels_height):
                for j in [0, window.pixels_width - 1]:
                    p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor, oblique_angle)

            # First and last line:
            for i in [0, window.pixels_height - 1]:
                for j in range(window.pixels_width):
                    p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor, oblique_angle)

                    # Alternating pixels
            for i in range(window.pixels_height):
                for j in range(1 + (i % 2), window.pixels_width, 2):
                    p[i][j] = self.cast_ray_for_pixel(window.get_pij(i, j), shadow, oblique, oblique_factor, oblique_angle)

            for i in range(0, window.pixels_height - 1):
                for j in range(2 - (i % 2), window.pixels_width - 1, 2):
                    mean1 = (p[i - 1][j] + p[i + 1][j]) / 2
                    mean2 = (p[i][j - 1] + p[i][j + 1]) / 2
                    diff1 = np.linalg.norm(p[i + 1][j] - p[i - 1][j])
                    diff2 = np.linalg.norm(p[i][j + 1] - p[i][j - 1])
                    if diff1 + diff2 != 0:
                        mean = (mean1 * diff2 + mean2 * diff1) / (diff1 + diff2)
                    else:
                        mean = mean1

                    p[i][j] = mean

        max_rgb = np.amax(np.amax(p, axis=0), axis=0)

        end = time.time()
        print("Done in: ", end - start)

        return p / [max(1, max_rgb[0]), max(1, max_rgb[1]), max(1, max_rgb[2])]

    def cast_ray_for_pixel(self, pij, shadow, oblique=False, oblique_factor=0., oblique_angle=0.):
        if oblique:
            r0 = pij
            d = np.array([-oblique_factor * math.cos(math.radians(oblique_angle)),
                          -oblique_factor * math.sin(math.radians(oblique_angle)),
                          -1])
            d /= np.linalg.norm(d)
        else:
            r0 = np.zeros(3)
            d = pij

        p_int, intersected_face = self.get_intersection(r0, d)

        return self.background_color if p_int is None else self.determine_color(r0, p_int, intersected_face, shadow)

    def determine_color(self, r0, p_int, intersected_face, shadow=True):
        """
        Return the RGB color for the pixel ij
        :param r0: origin of ray
        :param p_int: point intersected
        :param intersected_face: face intersected by the ray
        :param shadow: if True, consider shadow in calculation
        :return: pij rgb
        """
        pij_rgb = intersected_face.material.k_a_rgb * self.ambient_light
        for light_source in self.light_sources:

            if shadow:
                l_int, l_face = self.get_intersection(p_int, light_source.get_l(p_int), 0, intersected_face)

                if l_int is not None:
                    continue

                else:
                    pij_rgb += light_source.get_total_intensity(r0, intersected_face, p_int)
            else:
                pij_rgb += light_source.get_total_intensity(r0, intersected_face, p_int)

        return pij_rgb

    def get_intersection(self, r0, d, t_limit=1, face_int=None):
        objects_not_cut = self.objects_culling(r0, d)
        return self.get_intersected_face(objects_not_cut, r0, d, t_limit, face_int)

    def ray_touches_object(self, obj, r0, d):
        c = obj.center
        r = obj.radius

        a = d.dot(d)
        b = -2 * d.dot(r0 - c)
        c = (r0 - c).dot(r0 - c) - r ** 2

        return b ** 2 - 4 * a * c >= 0

    def objects_culling(self, r0, d):
        """
        Return objects that the ray intersects with their have intersection sphere(aura)
        :param pij: point corresponding to a pixel ij
        :return:
        """
        return [obj for obj in self.objects if self.ray_touches_object(obj, r0, d)]

    def find_t(self, face, r0, d):
        p1 = face.vertices[0].coordinates[:3]
        n = face.normal[:3]

        n_dot_d = np.dot(n, d[:3])
        if n_dot_d >= 0:
            return -1

        return n.dot(p1-r0)/n_dot_d

    def get_intersected_face(self, objects, r0, d, t_limit=1, face_int=None):
        """
        Returns witch faces have intersection with the ray and their point of intersection(t).
        :param objects: objects to check intersection with
        :param r0: origin of ray
        :param d: direction of ray
        :param t_limit: 1 if ray is from ray casting, 0 if is ray from light(shadow)
        :param face_int: when using ray from light to calculate shadow,
                face_int is the face where happened the intersection with ray from ray casting
        :return: point of intersection with the closest face and the face intersected
        """
        t_min = float('inf')
        intersected_face = (None, None)

        for object_ in objects:
            for face in [f for f in object_.faces if f is not face_int]:
                t = self.find_t(face, r0, d)

                if t < t_limit or (t_limit == 1 and t > t_min) or (t_limit == 0 and t > 1):
                    continue

                # ray and plane intersection point
                p = r0 + (t * d)

                # now we want to check if this point is inside the face
                if face.is_in_triangle(p):
                    t_min = t
                    intersected_face = (p, face)
                    if t_limit == 0:
                        return intersected_face

        return intersected_face

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


class LightSource(object):
    def __init__(self, intensity, position, direction=None):
        """
        :param intensity: light source intensity, between 0 and 1
        """
        self.intensity = np.array(intensity)
        self.position = np.append(position, [1])
        if direction is not None:
            self.direction = np.array(direction)/np.linalg.norm(direction)
        else:
            self.direction = None

    def get_l(self, p_int):
        return self.position[:3] - p_int

    def get_vectors(self, r0, face, p_int):
        """
        Return the unitary vectors n, l, u and r
        :param r0: origin of ray
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n_u = face.normal[:3]

        l = self.position[:3] - p_int
        l_u = (l / np.linalg.norm(l))

        v = r0-p_int
        v_u = (v / np.linalg.norm(v))

        r = 2 * (np.dot(l_u, n_u)) * n_u - l_u

        return n_u, l_u, v_u, r

    def get_total_intensity(self, r0, face, p_int):
        """
        Return the sum of the diffuse and specular term
        :param r0: origin of ray
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n, l, v, r = self.get_vectors(r0, face, p_int)

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
        :param position: position x,y,z of the light source
        """
        super().__init__(intensity, position, None)


class SpotLightSource(LightSource):
    def __init__(self, intensity, position, direction, theta):
        """
        :param intensity: light source intensity, between 0 and 1
        :param position: position x,y,z of the light source
        :param direction: direction vector of the light
        :param theta: limit angle at which light from source can be seen
        """
        super().__init__(intensity, position, direction)
        self.theta = theta

    def get_total_intensity(self, r0, face, p_int):
        """
        Return the sum of the diffuse and specular term
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n, l, v, r = self.get_vectors(r0, face, p_int)

        k_d_rgb = face.material.k_d_rgb
        k_e_rgb = face.material.k_e_rgb

        spot_intensity = self.direction.dot(-l)
        if spot_intensity < math.cos(math.radians(self.theta)):
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
        :param direction: direction vector of the light
        """
        super().__init__(intensity=intensity, position=None, direction=direction)

    def get_l(self, p_int):
        return -self.direction

    def get_vectors(self, r0, face, p_int):
        """
        Return the unitary vectors n, l, u and r
        :param r0: origin of ray
        :param face: face intersected by the ray
        :param p_int: point intersected
        :return:
        """
        n_u = face.normal[:3]

        l = -self.direction
        l_u = (l / np.linalg.norm(l))

        v = r0-p_int
        v_u = (v / np.linalg.norm(v))

        r = 2 * (np.dot(l_u, n_u)) * n_u - l_u

        return n_u, l_u, v_u, r
