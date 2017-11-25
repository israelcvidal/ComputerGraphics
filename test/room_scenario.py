import sys
sys.path.append("..")
from scenario.scenario import *
from transformations import model_transformations as mt
import copy
from objectModeling import obj


def create_objects():
    cube = obj.Obj().import_obj('../objects/cube.obj')

    objects = []

    S = mt.get_scale_matrix([3., 0.1, 4., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(S)
    objects.append(floor)

    T = mt.get_translation_matrix([0, 3., 0])
    roof = copy.deepcopy(floor)
    roof.apply_transformation(T)
    objects.append(roof)

    S = mt.get_scale_matrix([3., 0.3, 0.8, 1])
    T = mt.get_translation_matrix([0.1, 2.7, 0.1])
    M = mt.compose_matrices([T, S])
    roof_detail = copy.deepcopy(cube)
    roof_detail.apply_transformation(M)
    objects.append(roof_detail)

    S = mt.get_scale_matrix([0.5, 0.3, 4., 1])
    T = mt.get_translation_matrix([0.1, 2.7, 0])
    M = mt.compose_matrices([T, S])
    roof_detail2 = copy.deepcopy(cube)
    roof_detail2.apply_transformation(M)
    objects.append(roof_detail2)

    T = mt.get_translation_matrix([2.4, 0, 0])
    roof_detail3 = copy.deepcopy(roof_detail2)
    roof_detail3.apply_transformation(T)
    objects.append(roof_detail3)

    #T = mt.get_translation_matrix([0, 0, 3.2])
    #roof_detail4 = copy.deepcopy(roof_detail)
    #roof_detail4.apply_transformation(T)
    #objects.append(roof_detail4)

    S = mt.get_scale_matrix([3., 3., 0.1, 1])
    wall = copy.deepcopy(cube)
    wall.apply_transformation(S)
    objects.append(wall)

    S = mt.get_scale_matrix([0.1, 3., 4., 1])
    wall2 = copy.deepcopy(cube)
    wall2.apply_transformation(S)
    objects.append(wall2)

    T = mt.get_translation_matrix([2.9, 0, 0])
    wall3 = copy.deepcopy(wall2)
    wall3.apply_transformation(T)
    objects.append(wall3)

    #T = mt.get_translation_matrix([0, 0, 4.])
    #wall4 = copy.deepcopy(wall)
    #wall4.apply_transformation(T)
    #objects.append(wall4)

    S = mt.get_scale_matrix([0.75, 2.7, 0.2, 1])
    T = mt.get_translation_matrix([0, 0, 0.1])
    M = mt.compose_matrices([T, S])
    wall_detail = copy.deepcopy(cube)
    wall_detail.apply_transformation(M)
    objects.append(wall_detail)

    T = mt.get_translation_matrix([2.25, 0, 0])
    wall_detail2 = copy.deepcopy(wall_detail)
    wall_detail2.apply_transformation(T)
    objects.append(wall_detail2)

    S = mt.get_scale_matrix([0.5, 1., 0.2, 1])
    T = mt.get_translation_matrix([0.75, 1.7, 0.1])
    M = mt.compose_matrices([T, S])
    wall_detail3 = copy.deepcopy(cube)
    wall_detail3.apply_transformation(M)
    objects.append(wall_detail3)

    T = mt.get_translation_matrix([1., 0, 0])
    wall_detail4 = copy.deepcopy(wall_detail3)
    wall_detail4.apply_transformation(T)
    objects.append(wall_detail4)

    return objects

def main():
    d = 0.5
    window_height = 2.
    window_width = 2.
    pixels_height = 200
    pixels_width = 200

    objects = create_objects()

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[1.5, 2.9, 2.])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [1.5, 1.5, 7., 1.0]
    look_at = [1.5, 1.5, 1.5, 1.0]
    a_vup = [1.5, 5.5, 1.5, 1.0]
    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[1., 1., 1.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)

if __name__ == '__main__':
    main()