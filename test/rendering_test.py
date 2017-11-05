import sys
sys.path.append("..")
from scenario.scenario import *


def main():
    po = [10, 10, -5, 1.0]
    look_at = [0.5, 0.5, 0.5, 1.0]
    a_vup = [0.5, 3.0, 3.0, 1.0]
    d = 3.
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    red_material = obj.Material([1, 0, 0], [1, 0, 0], [1, 0, 0], 1)
    green_material = obj.Material([0, 1, 0], [0, 1, 0], [0, 1, 0], 1)
    blue_material = obj.Material([0, 0, 1], [0, 0, 1], [0, 0, 1], 1)
    yellow_material = obj.Material([1, 1, 0], [1, 1, 0], [1, 1, 0], 1)
    material = obj.Material([0.3, 0.6, 0.9], [0.3, 0.6, 0.9], [0.3, 0.6, 0.9], 1)
    white_material = obj.Material([1, 1, 1], [1, 1, 1], [1, 1, 1], 1)

    cube = obj.Obj()
    v1 = cube.add_vertex(0.0, 0.0, 0.0)
    v2 = cube.add_vertex(1.0, 0.0, 0.0)
    v3 = cube.add_vertex(0.0, 1.0, 0.0)
    v4 = cube.add_vertex(1.0, 1.0, 0.0)
    v5 = cube.add_vertex(0.0, 0.0, 1.0)
    v6 = cube.add_vertex(1.0, 0.0, 1.0)
    v7 = cube.add_vertex(0.0, 1.0, 1.0)
    v8 = cube.add_vertex(1.0, 1.0, 1.0)
    cube.add_face(v1, v4, v2, red_material)
    cube.add_face(v1, v3, v4, red_material)
    cube.add_face(v2, v8, v6, blue_material)
    cube.add_face(v2, v4, v8, blue_material)
    cube.add_face(v5, v6, v8, green_material)
    cube.add_face(v5, v8, v7, green_material)
    cube.add_face(v1, v5, v7, white_material)
    cube.add_face(v1, v7, v3, white_material)
    cube.add_face(v1, v2, v6, yellow_material)
    cube.add_face(v1, v6, v5, yellow_material)
    cube.add_face(v3, v7, v8, material)
    cube.add_face(v3, v8, v4, material)


    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[3.5, 3.5, 3.5])
    spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
                                 direction=[0.5, 0.5, 0.5], theta=20.0)
    infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    scenario = Scenario(objects=[cube], light_sources=[],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[1., 1., 1.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()