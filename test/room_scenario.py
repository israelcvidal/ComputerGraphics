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

    # T = mt.get_translation_matrix([0, 0, 3.2])
    # roof_detail4 = copy.deepcopy(roof_detail)
    # roof_detail4.apply_transformation(T)
    # objects.append(roof_detail4)

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

    # T = mt.get_translation_matrix([0, 0, 4.])
    # wall4 = copy.deepcopy(wall)
    # wall4.apply_transformation(T)
    # objects.append(wall4)

    S = mt.get_scale_matrix([0.5, 2.7, 0.3, 1])
    T = mt.get_translation_matrix([0, 0, 0.1])
    M = mt.compose_matrices([T, S])
    wall_detail = copy.deepcopy(cube)
    wall_detail.apply_transformation(M)
    objects.append(wall_detail)

    T = mt.get_translation_matrix([2.5, 0, 0])
    wall_detail2 = copy.deepcopy(wall_detail)
    wall_detail2.apply_transformation(T)
    objects.append(wall_detail2)

    S = mt.get_scale_matrix([0.5, 1., 0.3, 1])
    T = mt.get_translation_matrix([0.5, 1.7, 0.1])
    M = mt.compose_matrices([T, S])
    wall_detail3 = copy.deepcopy(cube)
    wall_detail3.apply_transformation(M)
    objects.append(wall_detail3)

    T = mt.get_translation_matrix([1.5, 0, 0])
    wall_detail4 = copy.deepcopy(wall_detail3)
    wall_detail4.apply_transformation(T)
    objects.append(wall_detail4)

    S = mt.get_scale_matrix([1., 0.06, 0.25, 1])
    T = mt.get_translation_matrix([1., 1.9, 0.1])
    M = mt.compose_matrices([T, S])
    shelf = copy.deepcopy(cube)
    shelf.apply_transformation(M)
    objects.append(shelf)

    T = mt.get_translation_matrix([0, 0.3, 0])
    shelf2 = copy.deepcopy(shelf)
    shelf2.apply_transformation(T)
    objects.append(shelf2)

    T = mt.get_translation_matrix([0, 0.3, 0])
    shelf3 = copy.deepcopy(shelf2)
    shelf3.apply_transformation(T)
    objects.append(shelf3)

    S = mt.get_scale_matrix([1., 0.6, 0.05, 1])
    T = mt.get_translation_matrix([1., 0.8, 0.1])
    M = mt.compose_matrices([T, S])
    tv = copy.deepcopy(cube)
    tv.apply_transformation(M)
    objects.append(tv)

    S = mt.get_scale_matrix([0.06, 0.6, 0.08, 1])
    T = mt.get_translation_matrix([0.94, 0.8, 0.1])
    M = mt.compose_matrices([T, S])
    tv_detail = copy.deepcopy(cube)
    tv_detail.apply_transformation(M)
    objects.append(tv_detail)

    T = mt.get_translation_matrix([1.06, 0, 0])
    tv_detail2 = copy.deepcopy(tv_detail)
    tv_detail2.apply_transformation(T)
    objects.append(tv_detail2)

    S = mt.get_scale_matrix([1.12, 0.06, 0.08, 1])
    T = mt.get_translation_matrix([0.94, 0.74, 0.1])
    M = mt.compose_matrices([T, S])
    tv_detail3 = copy.deepcopy(cube)
    tv_detail3.apply_transformation(M)
    objects.append(tv_detail3)

    T = mt.get_translation_matrix([0, 0.66, 0])
    tv_detail4 = copy.deepcopy(tv_detail3)
    tv_detail4.apply_transformation(T)
    objects.append(tv_detail4)

    S = mt.get_scale_matrix([1.2, 0.06, 0.4, 1])
    T = mt.get_translation_matrix([0.9, 0.2, 0.1])
    M = mt.compose_matrices([T, S])
    tv_rack = copy.deepcopy(cube)
    tv_rack.apply_transformation(M)
    objects.append(tv_rack)

    T = mt.get_translation_matrix([0, 0.2, 0])
    tv_rack2 = copy.deepcopy(tv_rack)
    tv_rack2.apply_transformation(T)
    objects.append(tv_rack2)

    S = mt.get_scale_matrix([0.06, 0.4, 0.35, 1])
    T = mt.get_translation_matrix([0.95, 0, 0.1])
    M = mt.compose_matrices([T, S])
    tv_rack3 = copy.deepcopy(cube)
    tv_rack3.apply_transformation(M)
    objects.append(tv_rack3)

    T = mt.get_translation_matrix([1.04, 0, 0])
    tv_rack4 = copy.deepcopy(tv_rack3)
    tv_rack4.apply_transformation(T)
    objects.append(tv_rack4)

    S = mt.get_scale_matrix([0.2, 0.9, 0.3, 1])
    T = mt.get_translation_matrix([0.6, 0, 0.1])
    M = mt.compose_matrices([T, S])
    speaker = copy.deepcopy(cube)
    speaker.apply_transformation(M)
    objects.append(speaker)

    T = mt.get_translation_matrix([1.6, 0, 0])
    speaker2 = copy.deepcopy(speaker)
    speaker2.apply_transformation(T)
    objects.append(speaker2)

    S = mt.get_scale_matrix([0.6, 0.2, 0.3, 1])
    T = mt.get_translation_matrix([1.2, 0.46, 0.1])
    M = mt.compose_matrices([T, S])
    device = copy.deepcopy(cube)
    device.apply_transformation(M)
    objects.append(device)

    return objects

def main():
    d = 2
    window_height = 2.
    window_width = 2.
    pixels_height = 200
    pixels_width = 200

    objects = create_objects()

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[1.5, 2.9, 2.])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [1.5, 1.5, 5.0, 1.0]
    look_at = [1.5, 1.5, 0, 1.0]
    a_vup = [1.5, 5.5, 1.5, 1.0]
    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[0., 0., 0.],
                        ambient_light=[1., 1., 1.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)

if __name__ == '__main__':
    main()