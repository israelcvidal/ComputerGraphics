import sys
sys.path.append("..")
from ray_casting.transformations import model_transformations as mt
import copy
from ray_casting.objectModeling import obj
from ray_casting.scenario.scenario import *


def main():
    d = 1
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    s = mt.get_scale_matrix([100., 0.1, 100., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(s)
    objects.append(floor)

    rgb_red = [1, 0, 0]
    red_material = obj.Material(rgb_red, rgb_red, [1,1,1], 1)

    T = mt.get_translation_matrix([50, 0, 50])
    S = mt.get_scale_matrix([1, 3, 1, 1])
    M = mt.compose_matrices([T, S])
    cube2 = copy.deepcopy(cube)
    cube2.apply_transformation(M)
    cube2.apply_material(red_material)
    objects.append(cube2)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[50.5, 5, 50.5])

    po = [50.5, 4, 60.5, 1.0]
    look_at = [50.5, 0., 50.5, 1.0]
    a_vup = [50.5, 20, 50.5, 1.0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    window = Window(window_width, window_height, d, pixels_width, pixels_height)

    scenario.render(window, ray_mean=False, parallel=False, shadow=True, projection_type="PERSPECTIVE", oblique_angle=None, oblique_factor=None)

if __name__ == '__main__':
    main()