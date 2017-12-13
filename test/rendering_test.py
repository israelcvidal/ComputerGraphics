import sys
sys.path.append("..")
from ray_casting.transformations import model_transformations as mt
import copy
from ray_casting.objectModeling import obj


def main():
    d = 0.5
    window_height = 1
    window_width = 1
    pixels_height = 300
    pixels_width = 300

    objects = []
    cube = obj.Obj().import_obj('../objects/cube.obj')

    # s = mt.get_scale_matrix([3., 0.1, 4., 1])
    # floor = copy.deepcopy(cube)
    # floor.apply_transformation(s)
    # objects.append(floor)

    # T = mt.get_translation_matrix([1, 0, 2])
    cube2 = copy.deepcopy(cube)
    cube2.apply_material(obj.Material([0, 0, 0], [0, 0, 0], [0, 0, 0], 1))
    # cube2.apply_transformation(T)
    objects.append(cube2)

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[1.5, 1.2, 0.1])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [1.5, 1.5, 1.5, 1.0]
    look_at = [1, 1, 1, 1.0]
    a_vup = [1, 2, 1, 1.0]

    p = "PERSPECTIVE"
    ob = "OBLIQUE"
    cb = "CABINET"
    cv = "CAVALIER"
    ort = "ORTHOGRAPHIC"

    projection_type = p

    scenario = Scenario(objects=objects, light_sources=[],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[1., 0., 0.],
                        ambient_light=[0.5, 0.5, 0.5])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height,
                    ray_mean=True, parallel=True, shadow=False, projection_type=projection_type,
                    oblique_angle=0, oblique_factor=0)



if __name__ == '__main__':
    main()