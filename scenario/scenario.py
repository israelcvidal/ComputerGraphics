import numpy as np
import math
import sys


class Scenario(object):
    def __init__(self, objects=[], light_sources=[], po=None, look_at=None, avup=None):
        """

        :param objects: list of all objects on the scenario
        :param light_sources: list of all light sources on the scenario
        :param po: observer(camera) location on world coordination
        :param look_at: loot at point
        :param avup: view up point
        """
        self.objects = objects
        self.light_sources = light_sources
        self.po = po
        self.look_at = look_at
        self.avup = avup

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
        p = np.ones((pixels_width, pixels_height))

        for i in range(pixels_height):
            y_i = (window_height / 2) - (delta_y / 2) - (i * delta_y)
            for j in range(pixels_width):
                x_i = (-window_width / 2) + (delta_x / 2) + (j * delta_x)
                p[i, j] = np.array([x_i, y_i, -window_distance]).transpose()
                p[i, j] = self.determine_color(p[i, j])

    def determine_color(self, pij):
        objects_not_cut = self.objects_culling(pij)
        faces_to_check_intersection = self.back_face_culling(objects_not_cut, pij)
        p_int, intersected_face = self.get_intersected_face(faces_to_check_intersection, pij)

        # TODO
        for light_source in self.light_sources:
            # determine rgb of pij
            pij_rgb = [1, 1, 1]

        return pij_rgb

    def objects_culling(self, pij):
        """
        Return objects that the ray intersects with their have intersection sphere(aura)
        :param pij: point corresponding to a pixel ij
        :return:
        """

        objects_not_cut = []

        for object_ in self.objects:
            vertices = np.array(object_.vertices.values())
            min_x = min(vertices[:, 0])
            max_x = max(vertices[:, 0])
            min_y = min(vertices[:, 1])
            max_y = max(vertices[:, 1])
            min_z = min(vertices[:, 2])
            max_z = max(vertices[:, 2])

            center = np.array([(max_x-min_x), (max_y-min_y), (max_z-min_z)])
            radius = math.pow((max_x-center[0]), 2)+math.pow((max_y-center[1]), 2)+math.pow((max_z-center[2]), 2)
            radius = math.sqrt(radius)
            a = pij.dot(pij)
            b = -2*(pij.dot(center))
            c = center.dot(center)-math.pow(radius, 2)
            if (math.pow(b, 2) - 4*a*c) >= 0:
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

        pij_u = pij/np.linalg.norm(pij)
        for object_ in objects:
            for face in object_.faces.values():
                if pij_u.dot(face.normal) < 0:
                    faces_not_cut.append(face)

        return faces_not_cut

    def get_intersected_face(self, faces, pij):
        """
        Returns witch faces have intersection with the ray and their point of intersection(t).
        :param faces:
        :return: point of intersection with the closest face and the face intersected
        """
        intersected_faces = []
        for face in faces:
            p1, p2, p3 = face.vertices
            t = face.normal.dot(p1)/face.normal.dot(pij)

            # ray and plane intersection point
            p = t*pij

            # now we want to check if this point is inside the face
            w1 = np.array(p1)-np.array(p)
            w2 = np.array(p2)-np.array(p)
            w3 = np.array(p3)-np.array(p)

            # checking normal of each new triangle
            n1 = np.cross(w1, w2)
            n2 = np.cross(w2, w3)
            n3 = np.cross(w3, w1)

            if n1.dot(n2) >= 0 and n2.dot(n3) >= 0:
                intersected_faces.append((t, face))

        intersected_face = min(intersected_faces, key=lambda f: f[0])
        return intersected_face[0]*pij, intersected_face[1]

    def render(self):
        pass

    # TODO
    def transform_to_camera(self):
        # transform all objects to camera
        pass

    # TODO
    def transform_to_world(self):
        # transform all objects to world
        pass


# TODO
class LightSource(object):
    pass


# TODO
class PunctualLightSource(LightSource):
    pass


# TODO
class SpotLightSource(LightSource):
    pass


# TODO
class InfinityLightSource(LightSource):
    pass
