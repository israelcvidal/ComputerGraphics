import sys
sys.path.append("..")
from transformations import world_camera_transformations as wct
from scenario import scenario as sc
import numpy as np
from objectModeling import obj
import math


def ap2(matricula):
    np.set_printoptions(suppress=True)

    F, E, D, C, B, A = matricula
    A = float(A)
    B = float(B)
    C = float(C)
    D = float(D)
    E = float(E)
    F = float(F)

    L = A+B+C+D+E+F
    P1 = np.array([A+10, B+5, 0, 1])
    P2 = P1 + np.array([L, 0, 0, 0])
    P3 = P1 + np.array([L/2, (L*math.sqrt(3))/2, 0, 0])
    P4 = P1 + np.array([L/2, (L*math.sqrt(3))/6, (L*math.sqrt(6))/6, 0])

    v1 = sc.obj.Vertex(0, P1)
    v2 = sc.obj.Vertex(1, P2)
    v3 = sc.obj.Vertex(2, P3)
    v4 = sc.obj.Vertex(3, P4)

    # k = np.array([1, 1, 1])
    # material = obj.Material(k, k, k, 2)
    # red_material = obj.Material([1, 0, 0], [1, 0, 0], [1, 0, 0], 1)
    # green_material = obj.Material([0, 1, 0], [0, 1, 0], [0, 1, 0], 1)
    # blue_material = obj.Material([0, 0, 1], [0, 0, 1], [0, 0, 1], 1)

    print("A: ", A)
    print("B: ", B)
    print("C: ", C)
    print("D: ", D)
    print("E: ", E)
    print("F: ", F)

    print("\nL: ", L)
    print("P1: ", P1)
    print("P2: ", P2)
    print("P3: ", P3)
    print("P4: ", P4)

    #QUESTAO 1:
    Po = np.array([A-5, B+L, (L*math.sqrt(6))/6, 1])
    Look_At = P4-np.array([0, 0, (L*math.sqrt(6))/6, 0])
    # View_Up = Look_At + np.array([0, 1, 0, 0])
    View_Up = P4

    print("\nPo: ", Po)
    print("Look_At: ", Look_At)
    print("View_Up: ", View_Up)

    # ITEM A)
    ic, jc, kc = wct.get_ijk(Po, Look_At, View_Up)
    print("\nITEM A)")
    print("ic: ", ic)
    print("jc: ", jc)
    print("kc: ", kc)

    # ITEM B)
    Mwc = wct.get_world_camera_matrix(Po[:3], Look_At[:3], View_Up[:3])
    Mcw = wct.get_camera_world_matrix(Po[:3], Look_At[:3], View_Up[:3])

    print("\nITEM B)")
    print("W->C:\n", Mwc)
    print("C->W:\n", Mcw)

    # ITEM C)
    print("ITEM C)")
    print("P1_c: ", Mwc.dot(P1))
    print("P2_c: ", Mwc.dot(P2))
    print("P3_c: ", Mwc.dot(P3))
    print("P4_c: ", Mwc.dot(P4))
    print("Po_c: ", Mwc.dot(Po))

    # QUESTAO 2:

    tetaedro = obj.Obj()
    k_a = np.array([A/50, B/50, C/50])
    k_d_s = 3*k_a
    m = 1
    ambient_light = np.array([0.4, 0.4, 0.4])

    pl_intensity = np.array([0.7, 0.7, 0.7])
    pl_position = np.array([A+10, B+L, 2*L])
    print("p_light position WORLD: ", pl_position)

    puntual_light = sc.PunctualLightSource(pl_intensity, pl_position)
    material = obj.Material(k_a, k_d_s, k_d_s, m)

    tetaedro.vertices = [v1, v2, v3, v4]
    tetaedro.add_face(v1, v2, v4, material)
    tetaedro.add_face(v1, v4, v3, material)
    tetaedro.add_face(v2, v3, v4, material)
    tetaedro.add_face(v1, v3, v2, material)

    P = P4-np.array([0, 0, (L*math.sqrt(6))/12, 0])
    Pc = Mwc.dot(P)
    print("\nP: ", P)
    print("Pc: ", Pc)

    scenario = sc.Scenario([tetaedro], [puntual_light], Po, Look_At, View_Up,
                           background_color=[0, 0, 0], ambient_light=ambient_light)
    # scenario.render(1, 1, 0.3, 200, 200)
    scenario.ray_casting_prova(Pc[:3])




if __name__ == '__main__':
    matricula = "751004"
    # matricula = "370019"

    ap2(matricula)


