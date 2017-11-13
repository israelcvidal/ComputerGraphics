import sys
sys.path.append("..")
from scenario.scenario import *


def main():
    d = 1.
    window_height = 1.
    window_width = 1.
    pixels_height = 200
    pixels_width = 200

    red_material = obj.Material([1, 0, 0], [1, 0, 0], [1, 0, 0], 1)
    green_material = obj.Material([0, 1, 0], [0, 1, 0], [0, 1, 0], 1)
    blue_material = obj.Material([0, 0, 1], [0, 0, 1], [0, 0, 1], 1)
    yellow_material = obj.Material([1, 1, 0], [1, 1, 0], [1, 1, 0], 1)
    material = obj.Material([0.3, 0.6, 0.9], [0.3, 0.6, 0.9], [0.3, 0.6, 0.9], 1)
    white_material = obj.Material([1, 1, 1], [1, 1, 1], [1, 1, 1], 1)
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
    cube.add_face(v1, v7, v5, material)
    cube.add_face(v1, v3, v7, material)

    # frente
    cube.add_face(v4, v5, v7, red_material)
    cube.add_face(v4, v7, v6, red_material)

    # esquerda
    cube.add_face(v0, v4, v6, blue_material)
    cube.add_face(v0, v6, v2, blue_material)

    # baixo
    cube.add_face(v0, v1, v5, green_material)
    cube.add_face(v0, v5, v4, green_material)

    # cima
    cube.add_face(v2, v6, v7, yellow_material)
    cube.add_face(v2, v7, v3, yellow_material)

    cube2 = obj.Obj()
    v0 = cube2.add_vertex(0.0, 0.0, 0.0)
    v1 = cube2.add_vertex(1.0, 0.0, 0.0)
    v2 = cube2.add_vertex(0.0, 1.0, 0.0)
    v3 = cube2.add_vertex(1.0, 1.0, 0.0)
    v4 = cube2.add_vertex(0.0, 0.0, 1.0)
    v5 = cube2.add_vertex(1.0, 0.0, 1.0)
    v6 = cube2.add_vertex(0.0, 1.0, 1.0)
    v7 = cube2.add_vertex(1.0, 1.0, 1.0)

    # trás
    cube2.add_face(v0, v3, v1, orange_material)
    cube2.add_face(v0, v2, v3, orange_material)

    # direita
    cube2.add_face(v1, v7, v5, material)
    cube2.add_face(v1, v3, v7, material)

    # frente
    cube2.add_face(v4, v5, v7, red_material)
    cube2.add_face(v4, v7, v6, red_material)

    # esquerda
    cube2.add_face(v0, v4, v6, blue_material)
    cube2.add_face(v0, v6, v2, blue_material)

    # baixo
    cube2.add_face(v0, v1, v5, green_material)
    cube2.add_face(v0, v5, v4, green_material)

    # cima
    cube2.add_face(v2, v6, v7, yellow_material)
    cube2.add_face(v2, v7, v3, yellow_material)

    from transformations import model_transformations as mt

    T = mt.get_translation_matrix([0, 1., 0])
    R = mt.get_rotation_matrix(90, axis='x')
    M = mt.compose_matrices([T])
    for vertex in cube2.vertices:
        vertex.coordinates = M.dot(vertex.coordinates)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[30, -5, 0.5])
    spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
                                 direction=[0.5, 0.5, 0.5], theta=20.0)
    infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [5, 0.5, 0.5, 1.0]
    look_at = [0.5, 0.5, 0.5, 1.0]
    a_vup = [0.5, 3, 0.5, 1.0]
    scenario = Scenario(objects=[cube, cube2], light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0., 0., 0.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()