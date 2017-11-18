import sys
sys.path.append("..")
from scenario.scenario import *
from transformations import model_transformations as mt
import copy

def main():
    d = 3
    window_height = 2.
    window_width = 2.
    pixels_height = 200
    pixels_width = 200

    # red_material = obj.Material([1, 0, 0], [1, 0, 0], [1, 0, 0], 1)
    # green_material = obj.Material([0, 1, 0], [0, 1, 0], [0, 1, 0], 1)
    # blue_material = obj.Material([0, 0, 1], [0, 0, 1], [0, 0, 1], 1)
    # yellow_material = obj.Material([1, 1, 0], [1, 1, 0], [1, 1, 0], 1)
    # material = obj.Material([0.3, 0.6, 0.9], [0.3, 0.6, 0.9], [0.3, 0.6, 0.9], 1)
    # white_material = obj.Material([1, 1, 1], [1, 1, 1], [1, 1, 1], 1)
    orange_material = obj.Material([1.0, 140.0/255.0, 0.0], [1.0, 140.0/255.0, 0.0], [1.0, 140.0/255.0, 0.0], 1)

    cube = obj.Obj()
    v0 = cube.add_vertex(0.0, 0.0, 0.0)
    v1 = cube.add_vertex(1.0, 0.0, 0.0)
    v2 = cube.add_vertex(0.0, 1.0, 0.0)
    v3 = cube.add_vertex(1.0, 1.0, 0.0)
    v4 = cube.add_vertex(0.0, 0.0, 1.0)
    v5 = cube.add_vertex(1.0, 0.0, 1.0)
    v6 = cube.add_vertex(0.0, 1.0, 1.0)
    v7 = cube.add_vertex(1.0, 1.0, 1.0)

    # trás
    cube.add_face(v0, v3, v1, orange_material)
    cube.add_face(v0, v2, v3, orange_material)

    # direita
    cube.add_face(v1, v7, v5, orange_material)
    cube.add_face(v1, v3, v7, orange_material)

    # frente
    cube.add_face(v4, v5, v7, orange_material)
    cube.add_face(v4, v7, v6, orange_material)

    # esquerda
    cube.add_face(v0, v4, v6, orange_material)
    cube.add_face(v0, v6, v2, orange_material)

    # baixo
    cube.add_face(v0, v1, v5, orange_material)
    cube.add_face(v0, v5, v4, orange_material)

    # cima
    cube.add_face(v2, v6, v7, orange_material)
    cube.add_face(v2, v7, v3, orange_material)

    objects = []

    S = mt.get_scale_matrix([4., 0.1, 3., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(S)
    objects.append(floor)

    T = mt.get_translation_matrix([0, 3., 0])
    roof = copy.deepcopy(floor)
    roof.apply_transformation(T)
    objects.append(roof)

    S = mt.get_scale_matrix([4., 0.3, 0.5, 1])
    T = mt.get_translation_matrix([0, 2.7, 0])
    M = mt.compose_matrices([T, S])
    roof_detail = copy.deepcopy(cube)
    roof_detail.apply_transformation(M)
    objects.append(roof_detail)

    S = mt.get_scale_matrix([0.5, 0.3, 3., 1])
    T = mt.get_translation_matrix([0, 2.7, 0])
    M = mt.compose_matrices([T, S])
    roof_detail2 = copy.deepcopy(cube)
    roof_detail2.apply_transformation(M)
    objects.append(roof_detail2)

    T = mt.get_translation_matrix([3.5, 0, 0])
    roof_detail3 = copy.deepcopy(roof_detail2)
    roof_detail3.apply_transformation(T)
    objects.append(roof_detail3)

    S = mt.get_scale_matrix([4., 3., 0.1, 1])
    wall = copy.deepcopy(cube)
    wall.apply_transformation(S)
    objects.append(wall)

    S = mt.get_scale_matrix([0.1, 3., 3., 1])
    wall2 = copy.deepcopy(cube)
    wall2.apply_transformation(S)
    objects.append(wall2)

    T = mt.get_translation_matrix([3.9, 0, 0])
    wall3 = copy.deepcopy(wall2)
    wall3.apply_transformation(T)
    objects.append(wall3)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[2, 2.9, 1.5])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [2, 2, 10, 1.0]
    look_at = [2, 2, 2, 1.0]
    a_vup = [2, 5.5, 2, 1.0]
    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[1., 1., 1.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()