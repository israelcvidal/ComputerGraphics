import numpy as np

from ray_casting.objectModeling import obj
from ray_casting.scenario import scenario as sc
from ray_casting.transformations import world_camera_transformations as wct


def ap2(matricula):
    F, E, D, C, B, A = matricula
    A = float(A)
    B = float(B)
    C = float(C)
    D = float(D)
    E = float(E)
    F = float(F)

    eye = np.array([0, 0, 0])
    rgb_ambient = np.array([0.5, 0.5, 0.5])
    punctual_intensity = np.array([0.9, 0.8, 1.0])
    punctual_position = np.array([-4., 6., -3.])
    punctual_light = sc.PunctualLightSource(punctual_intensity, punctual_position)
    light_sources = [punctual_light]

    look_at = np.array([D, E, F])
    view_up = np.array(([A, B, C]))
    m = 2.0
    material = obj.Material([0.8, 0.3, 0.2], [0.8, 0.3, 0.2], [0.8, 0.3, 0.2], m)

    d = 3.
    w = 8.
    h = 8.
    w_pixels = 800
    h_pixels = 800

    t_int = 12
    i = 1
    j = 3


    # CHECK IF NORMAL IS IN CAMERA OR WORLD!!!!!
    se = [-4, 4, -3]
    face = obj.Face(0, None, material, None)

    # Getting i,j,k vectors
    ic, jc, kc = wct.get_ijk(eye, look_at, view_up)

    # Getting w<->c matrices
    M_w_c = wct.get_world_camera_matrix(eye, look_at, view_up)
    M_c_w = wct.get_camera_world_matrix(eye, look_at, view_up)

    # RAY CASTING

    delta_w = w / w_pixels
    delta_h = h / h_pixels

    y_i = (h / 2) - (delta_h / 2) - i * delta_h
    x_ij = (-w / 2) + (delta_w/ 2) + j * delta_w

    p_ij = np.array([x_ij, y_i, -d])

    # IF NOT IN CAMERA POSITION:
    for light_source in light_sources:
        light_source.position = M_w_c.dot(light_source.position)

    print("ic:")
    print(ic)
    print("jc:")
    print(jc)
    print("kc:")
    print(kc)

    print("\nMatrix camera->world:")
    print(M_c_w)
    print("Matrix world->camera:")
    print(M_w_c)

    print("\npij:")
    print(p_ij)

    p_ij = p_ij / np.linalg.norm(p_ij)

    if t_int:
        p = t_int * p_ij
    else:
        t_int = np.dot(face.normal, face.vertices[0][:3]) / np.dot(face.normal, p_ij[:3])
        p = t_int * p_ij

    print("pint:")
    print(p)

    normal = (se - p) / np.linalg.norm(se - p)
    face.normal = normal
    print("face.normal:")
    print(face.normal)

    for light_source in light_sources:
        _, l, v, r = light_source.get_vectors(face, p)
        print("l:")
        print(l)
        print("v:")
        print(v)
        print("r:")
        print(r)

    pij_rgb = face.material.k_a_rgb * rgb_ambient
    print("ambient: ")
    print(pij_rgb)
    for light_source in light_sources:
        pij_rgb += light_source.get_total_intensity(face, p)

    print("\npij_rgb:")
    print(pij_rgb)


if __name__ == '__main__':
    matricula = "751004"

    ap2(matricula)


