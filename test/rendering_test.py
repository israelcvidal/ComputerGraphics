import sys
sys.path.append("..")
from scenario.scenario import *
from transformations import model_transformations as mt
import copy
from objectModeling import obj

def main():
    d = 0.3
    window_height = 1.
    window_width = 1.
    pixels_height = 200
    pixels_width = 200

    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    s = mt.get_scale_matrix([3., 0.1, 4., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(s)
    objects.append(floor)

    T = mt.get_translation_matrix([0, 0, 2])
    cube2 = copy.deepcopy(cube)
    cube2.apply_transformation(T)
    objects.append(cube2)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[0.5, 1., 0])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [1.5, 1.5, 5, 1.0]
    look_at = [1.5, 2, 0, 1.0]
    a_vup = [1.5, 3, 0, 1.0]
    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[0.0, 0.0, 0.0])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()