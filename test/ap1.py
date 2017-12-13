import sys
sys.path.append("..")
from ray_casting.transformations.model_transformations import *


def prova(matricula):
    F, E, D, C, B, A = matricula
    A = int(A)
    B = int(B)
    C = int(C)
    D = int(D)
    E = int(E)
    F = int(F)

    print(A, B, C, D, E, F)

    p1 = np.array([0, 0, 0, 1])
    p2 = np.array([0, 0, 2+A, 1])
    p3 = np.array([3+B, 0, 0, 1])
    p4 = np.array([0, 1+C, 0, 1])
    p3_ = np.array([30*(1+D), 10*(2+F), 0, 1])

    scale_matrix = get_scale_matrix(np.array([5*math.sqrt(2)/p3[0], 5*math.sqrt(2)/p4[1], 5*math.sqrt(2)/p2[2], 1]))
    print("scale matrix:\n", scale_matrix)
    p1 = scale_matrix.dot(p1)
    p2 = scale_matrix.dot(p2)
    p3 = scale_matrix.dot(p3)
    p4 = scale_matrix.dot(p4)

    print("\nscaled points:")

    for p in [p2, p3, p4]:
        print(p)

    print("\ntranslation _p3->origin:")
    translation_p3_o = get_translation_matrix(-p3[:3])
    print(translation_p3_o)

    N = np.cross((p3-p2)[0:3], (p4-p2)[:3])
    n = N/np.linalg.norm(N)
    print("n: ", n)
    n_after = np.array([0, 0, -1])
    theta = np.rad2deg(math.acos(n.dot(n_after)))

    quaternion_matrix = get_quaternion_matrix(p3[:3], p4[:3], theta)
    print("\nquaternion matrix - angle " + str(theta))
    print(quaternion_matrix)

    #vetor unitário na direção de p2:
    u_o_p2 = np.array([math.sin(np.radians(15)), math.cos(np.radians(15)), 0])

    # vetor unitário na direção do p3_:
    u_o_p3_ = p3_[:3]/np.linalg.norm(p3_[:3])

    # angulo entre os dois vetores unitários:
    alpha = np.rad2deg(math.acos(u_o_p3_.dot(u_o_p2)))

    rotation_z = get_rotation_matrix(-alpha, "z")
    print("\nrotation z - angle " + str(alpha))
    print(rotation_z)

    translation_o_p3 = get_translation_matrix(p3_[:3])
    print("\ntranslation matrix: ")
    print(translation_o_p3)
    matrix = compose_matrices([translation_o_p3,  rotation_z, quaternion_matrix, translation_p3_o])

    print("\npoints after transformations:")
    points = [p1, p2, p3, p4]
    for i, p in enumerate(points):
        points[i] = matrix.dot(p)
        print("p" + str(i+1) + ": ")
        print(points[i])

    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    translation_p1_o = get_translation_matrix(-p1[:3])
    translation_o_p1 = get_translation_matrix(p1[:3])

    mirror_matrix = get_arbitrary_mirror_matrix((p2-p1)[:3], (p4-p1)[:3])
    print("\ntranslation matrix: ")
    print(translation_p1_o)

    print("\nmirror matrix: ")
    print(mirror_matrix)

    print("\ninverse translation matrix:")
    print(translation_o_p1)

    print(compose_matrices([translation_o_p1, mirror_matrix, translation_p1_o]).dot(p3_))


if __name__ == '__main__':
    matricula = "370019"
    # matricula = "362955"
    # matricula = "344077"
    prova(matricula)
