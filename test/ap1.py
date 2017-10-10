from transformation.transformation import *


def prova():
    p1 = np.array([0, 0, 0, 1])
    p2 = np.array([0, 0, 11, 1])
    p3 = np.array([4, 0, 0, 1])
    p4 = np.array([0, 1, 0, 1])
    p3_ = np.array([30, 50, 0, 1])

    scale_matrix = get_scale_matrix(np.array([5*math.sqrt(2)/4, 5*math.sqrt(2), 5*math.sqrt(2)/11, 1]))
    print("scale matrix:\n", scale_matrix)
    _p1 = scale_matrix.dot(p1)
    _p2 = scale_matrix.dot(p2)
    _p3 = scale_matrix.dot(p3)
    _p4 = scale_matrix.dot(p4)

    print("\nscaled points:")

    for p in [_p2, _p3, _p4]:
        print(p)

    print("\ntranslation _p3->origin:")
    translation_p3_o = get_translation_matrix(-_p3[:3])
    print(translation_p3_o)

    N = np.cross((_p3-_p2)[0:3], (_p4-_p2)[:3])
    n = N/np.linalg.norm(N)
    n_after = np.array([0, 0, -1])
    theta = np.degrees(math.acos(n.dot(n_after)))

    quaternion_matrix = get_quaternion_matrix(_p3[:3], _p4[:3], theta)
    print("\nquaternion matrix - angle " + str(theta))
    print(quaternion_matrix)

    #vetor unitário na direção de p2:
    u_o_p2 = np.array([math.sin(np.radians(15)), math.cos(np.radians(15)), 0])

    # vetor unitário na direção do p3_:
    u_o_p3_ = p3_[:3]/np.linalg.norm(p3_[:3])

    # angulo entre os dois vetores unitários:
    alpha = np.degrees(math.acos(u_o_p3_.dot(u_o_p2)))

    rotation_z = get_rotation_matrix(-alpha, "z")
    print("\nrotation z:")
    print(rotation_z)

    translation_o_p3 = get_translation_matrix(p3_[:3])

    matrix = compose_matrices([translation_o_p3,  rotation_z, quaternion_matrix, translation_p3_o])

    print("\npoints after transformation:")
    points = [_p1, _p2, _p3, _p4]
    for i, p in enumerate(points):
        points[i] = matrix.dot(p)
        print("p" + str(i+1) + ": ")
        print(points[i])


if __name__ == '__main__':
    prova()