import sys
sys.path.append("..")
from ray_casting.transformations import model_transformations as mt
import copy
from ray_casting.objectModeling import obj
from ray_casting.scenario.scenario import *


def one_vanishing_point():
    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    color = np.array([254, 178, 76]) / 255
    color_material = obj.Material(color, color, [0.8, 0.8, 0.8], 10)
    # BAIXO
    S = mt.get_scale_matrix([10, 0.1, 10., 1])
    T = mt.get_translation_matrix([0.0, 0.0, 0.])
    M = mt.compose_matrices([T, S])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(M)
    floor.apply_material(color_material)
    objects.append(floor)

    # DIREITA
    T = mt.get_translation_matrix([10, 0.1, 0.])
    S = mt.get_scale_matrix([0.1, 10, 10, 1])
    M = mt.compose_matrices([T, S])
    cube2 = copy.deepcopy(cube)
    cube2.apply_transformation(M)
    cube2.apply_material(color_material)
    objects.append(cube2)

    # ESQUERDA
    T = mt.get_translation_matrix([-0.1, 0.1, 0.])
    S = mt.get_scale_matrix([0.1, 10, 10, 1])
    M = mt.compose_matrices([T, S])
    cube3 = copy.deepcopy(cube)
    cube3.apply_transformation(M)
    cube3.apply_material(color_material)
    objects.append(cube3)

    # CIMA
    T = mt.get_translation_matrix([0, 10.1, 0])
    S = mt.get_scale_matrix([10, 0.1, 10, 1])
    M = mt.compose_matrices([T, S])
    cube4 = copy.deepcopy(cube)
    cube4.apply_transformation(M)
    cube4.apply_material(color_material)
    objects.append(cube4)

    punctual_light = PunctualLightSource(intensity=[0.5, 0.5, 0.5], position=[5., 8., 20.])

    punctual_light2 = PunctualLightSource(intensity=[0.5, 0.5, 0.5], position=[20., 20., 5.])

    d = 1
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    window = Window(window_width, window_height, d, pixels_width, pixels_height)

    # # ONE VANISHING POINT
    po = [5., 5., 25, 1.0]
    look_at = [5., 5., 0, 1.0]
    a_vup = [5., 6, 0, 1.0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light, punctual_light2],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    scenario.render(window, ray_mean=False, parallel=True, shadow=True, projection_type="PERSPECTIVE",
                    oblique_angle=None, oblique_factor=None)


def two_vanishing_points():
    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    color = np.array([254, 178, 76]) / 255
    color_material = obj.Material(color, color, [0.8, 0.8, 0.8], 10)

    S = mt.get_scale_matrix([10, 10, 10., 1])
    T = mt.get_translation_matrix([0.0, 0.0, 0.])
    M = mt.compose_matrices([T, S])
    cube.apply_transformation(M)
    cube.apply_material(color_material)
    objects.append(cube)


    punctual_light = PunctualLightSource(intensity=[0.5, 0.5, 0.5], position=[20., 20., 5.])

    d = 1
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    window = Window(window_width, window_height, d, pixels_width, pixels_height)

    # TWO VANISHING POINTS
    po = [30., 30., 5, 1.0]
    look_at = [5., 5., 5, 1.0]
    a_vup = [5., 5, 6., 1.0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    scenario.render(window, ray_mean=False, parallel=True, shadow=True, projection_type="PERSPECTIVE",
                    oblique_angle=None, oblique_factor=None)


def three_vanishing_points():
    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    color = np.array([254, 178, 76]) / 255
    color_material = obj.Material(color, color, [0.8, 0.8, 0.8], 10)

    S = mt.get_scale_matrix([10, 10, 10., 1])
    T = mt.get_translation_matrix([0.0, 0.0, 0.])
    M = mt.compose_matrices([T, S])
    cube.apply_transformation(M)
    cube.apply_material(color_material)
    objects.append(cube)

    punctual_light = PunctualLightSource(intensity=[0.5, 0.5, 0.5], position=[20., 20., 5.])

    d = 1
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    window = Window(window_width, window_height, d, pixels_width, pixels_height)

    # THREE VANISHING POINTS

    po = [20., 20., 20., 1.0]
    look_at = [10., 10., 10, 1.0]
    a_vup = [10., 12, 10, 1.0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    scenario.render(window, ray_mean=False, parallel=True, shadow=True, projection_type="PERSPECTIVE",
                    oblique_angle=None, oblique_factor=None)


def main():
    one_vanishing_point()
    two_vanishing_points()
    three_vanishing_points()


if __name__ == '__main__':
    main()
