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
    pixels_height = 300
    pixels_width = 300

    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    s = mt.get_scale_matrix([100., 0.1, 100., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(s)
    objects.append(floor)

    T = mt.get_translation_matrix([50, 2, 50])
    cube2 = copy.deepcopy(cube)
    cube2.apply_transformation(T)
    objects.append(cube2)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[50, 3.5, 48])

    po = [50, 3, 85, 1.0]
    look_at = [50, 0.5, 50, 1.0]
    a_vup = [50, 2, 50, 1.0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height,
                    ray_mean=False, parallel=True, shadow=True, projection_type="PERSPECTIVE",
                    oblique_angle=0, oblique_factor=None)


if __name__ == '__main__':
    main()