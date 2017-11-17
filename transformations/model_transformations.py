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


def get_rotation_matrix(theta=None, axis=None, sin=None, cos=None):
    # If axis == x, y or z:

    rotation_matrix = np.identity(4)

    if sin is None and cos is None:
        sin = math.sin(np.radians(theta))
        cos = math.cos(np.radians(theta))

    if axis == 'x':
        rotation_matrix[1, 1] = cos
        rotation_matrix[1, 2] = -sin
        rotation_matrix[2, 1] = sin
        rotation_matrix[2, 2] = cos

    elif axis == 'y':
        rotation_matrix[0, 0] = cos
        rotation_matrix[0, 2] = sin
        rotation_matrix[2, 0] = -sin
        rotation_matrix[2, 2] = cos

    elif axis == 'z':
        rotation_matrix[0, 0] = cos
        rotation_matrix[0, 1] = -sin
        rotation_matrix[1, 0] = sin
        rotation_matrix[1, 1] = cos

    else:
        raise Exception("axis must be 'x', 'y', 'z' or None")

    return rotation_matrix


def get_arbitrary_rotation_matrix(p1, p2, theta):
    """
    Rotation of a point in 3 dimensional space by theta about an arbitrary axes
    defined by a line between two points P1 = (x1,y1,z1) and P2 = (x2,y2,z2).

    (1) translate space so that the rotation axis passes through the origin
    (2) rotate space about the x axis so that the rotation axis lies in the xz plane

    (3) rotate space about the y axis so that the rotation axis lies along the z axis

    (4) perform the desired rotation by theta about the z axis

    (5) apply the inverse of step (3)

    (6) apply the inverse of step (2)

    (7) apply the inverse of step (1)

    :param p1: points that form the arbitrary line.
    :param p2: points that form the arbitrary line.
    :param theta: angle of rotation
    :return:
    """
    # (1)
    # getting the translation matrices needed for (1) and (7)
    translation_matrix = get_translation_matrix(-1*np.array(p1))
    inverse_translation_matrix = get_translation_matrix(np.array(p1))

    # (2)
    # Let U = (a,b,c) be the unit vector along the rotation axis.
    # define d = sqrt(b^2 + c^2) as the length of the projection onto the yz plane
    rotation_axis = np.array(p2) - np.array(p1)
    a, b, c = rotation_axis
    d = math.sqrt(b**2 + c**2)
    x_rotation_matrix = get_rotation_matrix(axis='x', sin=b/d, cos=c/d)
    x_inverse_rotation_matrix = np.array(x_rotation_matrix)
    x_inverse_rotation_matrix[1, 2] *= -1
    x_inverse_rotation_matrix[2, 1] *= -1

    # (3)
    sin = a/np.linalg.norm(rotation_axis)
    cos = d/np.linalg.norm(rotation_axis)
    y_rotation_matrix = get_rotation_matrix(axis='y', sin=-sin, cos=cos)
    y_inverse_rotation_matrix = np.array(y_rotation_matrix)
    y_inverse_rotation_matrix[0, 2] *= -1
    y_inverse_rotation_matrix[2, 0] *= -1

    # (4)
    z_rotation_matrix = get_rotation_matrix(axis='z', theta=theta)

    result_matrix = compose_matrices([inverse_translation_matrix, x_inverse_rotation_matrix,
                                      y_inverse_rotation_matrix, z_rotation_matrix,
                                      y_rotation_matrix, x_rotation_matrix, translation_matrix])

    return result_matrix


def get_quaternion_matrix(p1, p2, theta):
    """
    (1) translate p1 to origin
    (2) calculate unit vector u=p1p2
    (3) q = (cos(theta/2), sin(theta/2)*u
    (4) q*=(cos(theta/2), -sin(theta/2)*u
    (5) return [t_inv][Lq][Rq*][t]
    :param p1:
    :param p2:
    :param theta:
    :return:
    """
    half_theta = np.radians(theta/2)
    p1 = np.array(p1)
    p2 = np.array(p2)
    # (1)
    translation_matrix = get_translation_matrix(-1*np.array(p1))
    inverse_translation_matrix = get_translation_matrix(np.array(p1))

    # (2)
    # unit rotation axis
    u = (p2-p1)/np.linalg.norm(p2-p1)

    # (3)
    q = np.array(list((math.sin(half_theta) * u)) + [math.cos(half_theta)])

    # (4)
    q_ = np.array(list((-math.sin(half_theta) * u)) + [math.cos(half_theta)])

    # (5) getting Lq and Rq*
    x = 0
    y = 1
    z = 2
    w = 3

    L_q = np.array([[q[w], -q[z], q[y], q[x]],
                    [q[z], q[w], -q[x], q[y]],
                    [-q[y], q[x], q[w], q[z]],
                    [-q[x], -q[y], -q[z], q[w]]]
                   )

    R_q_ = np.array([[q_[w], q_[z], -q_[y], q_[x]],
                    [-q_[z], q_[w], q_[x], q_[y]],
                    [q_[y], -q_[x], q_[w], q_[z]],
                    [-q_[x], -q_[y], -q_[z], q_[w]]]
                    )

    # return compose_matrices([inverse_translation_matrix, L_q, R_q_, translation_matrix])
    return compose_matrices([L_q, R_q_])


def get_translation_matrix(t):
    if len(t) != 3:
        raise Exception("Invalid number of arguments to generate translation matrix. Must be 3")

    translation_matrix = np.identity(4)

    for i in range(len(t)):
        translation_matrix[i, 3] = t[i]

    return translation_matrix


def get_mirror_matrix(u, v):
    # e.g.: u = 'x', v = 'y'
    mirror_matrix = np.identity(4)

    plane = [get_axis(i) for i in [u, v]]

    for i in range(len(mirror_matrix)-1):
        if i not in plane:
            mirror_matrix[i, i] = -1
    return mirror_matrix


def get_arbitrary_mirror_matrix(u, v):
    # Translate mirror to origin
    translation_matrix = get_translation_matrix(-1 * np.array(u))
    inverse_translation_matrix = get_translation_matrix(np.array(u))

    n = np.cross(u, v)
    n = (n / np.linalg.norm(n)).reshape(3, 1)

    mirror_matrix = np.identity(4)
    mirror_matrix[:3, :3] = np.identity(3) - (2*np.dot(n, np.transpose(n)))
    # return compose_matrices([inverse_translation_matrix, mirror_matrix, translation_matrix])
    return mirror_matrix


# cisalhamento no eixo 'axis' esbarrando em 'direction'
def get_shear_matrix(axis, direction, alpha):
    shear_matrix = np.identity(4)
    i = get_axis(direction)
    j = get_axis(axis)

    shear_matrix[i, j] = math.tan(np.radians(alpha))

    return shear_matrix


def compose_matrices(args):
    # [Tn...T3, T2, T1]
    result_matrix = args.pop(0)

    for matrix in args:
        result_matrix = np.dot(result_matrix, matrix)

    return result_matrix


def get_axis(axis):
    dic = {'x': 0, 'y': 1, 'z': 2}
    return dic[axis]


def transform_4d(point):
    if len(point) == 3:
        return np.array(list(point)+[0])
    elif len(point) == 4:
        warnings.warn("point already have 3 dimensions")
        return point
    else:
        raise Exception("Point must have 3 dimensions")

