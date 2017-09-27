import numpy as np
import warnings
import math


def get_scale_matrix(e):
    """
    :param e: list of 4 arguments to form the scale matrix
    :return:
    """

    if len(e) != 4:
        raise Exception("Invalid number of arguments to generate scale matrix. Must be 4")

    scale_matrix = np.identity(4)

    for i in range(len(e)):
        scale_matrix[i, i] = e[i]

    return scale_matrix


def get_rotation_matrix(theta, axis):
    # If axis == x, y or z:
    if axis:
        rotation_matrix = np.identity(4)

        if axis == 'x':
            rotation_matrix[1, 1] = math.cos(theta)
            rotation_matrix[1, 2] = -math.sin(theta)
            rotation_matrix[2, 1] = math.sin(theta)
            rotation_matrix[2, 2] = math.cos(theta)

        elif axis == 'y':
            rotation_matrix[0, 0] = math.cos(theta)
            rotation_matrix[0, 2] = math.sin(theta)
            rotation_matrix[2, 0] = -math.sin(theta)
            rotation_matrix[2, 2] = math.cos(theta)

        elif axis == 'z':
            rotation_matrix[0, 0] = math.cos(theta)
            rotation_matrix[0, 1] = -math.sin(theta)
            rotation_matrix[1, 0] = math.sin(theta)
            rotation_matrix[1, 1] = math.cos(theta)

        else:
            raise Exception("axis must be 'x', 'y', 'z' or None")

        return rotation_matrix

    # if we want a rotation about an arbitrary axis
    # todo:
    else:
        pass


def get_translation_matrix(t):
    if len(t) != 3:
        raise Exception("Invalid number of arguments to generate translation matrix. Must be 3")

    translation_matrix = np.identity(4)

    for i in range(len(t)):
        translation_matrix[i, 3] = t[i]

    return translation_matrix


def get_mirror_matrix(plane):
    mirror_matrix = np.identity(4)

    plane = [get_axis(i) for i in plane]

    for i in range(len(mirror_matrix)-1):
        if i not in plane:
            mirror_matrix[i, i] = -1
    return mirror_matrix


# cisalhamento no eixo 'axis' esbarrando em 'direction'
def get_shear_matrix(axis, direction, alpha):
    shear_matrix = np.identity(4)
    i = get_axis(direction)
    j = get_axis(axis)

    shear_matrix[i, j] = math.tan(alpha)

    return shear_matrix


def compose_matrices(args):
    np.multiply()


def get_axis(axis):
    dic = {'x': 0, 'y': 1, 'z': 2}
    return dic[axis]


if __name__ == '__main__':
    print(get_shear_matrix('z', 'y', math.radians(60)))
