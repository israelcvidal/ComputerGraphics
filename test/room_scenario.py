import sys
sys.path.append("..")
from scenario.scenario import *
from transformations import model_transformations as mt
import copy
from objectModeling import obj


def create_objects():
    cube = obj.Obj().import_obj('../objects/cube.obj')

    objects = []

    # CHÃO
    s = mt.get_scale_matrix([3., 0.1, 4., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(s)
    objects.append(floor)

    # TETO
    t = mt.get_translation_matrix([0, 3., 0])
    roof = copy.deepcopy(floor)
    roof.apply_transformation(t)
    objects.append(roof)

    s = mt.get_scale_matrix([3., 0.3, 0.8, 1])
    t = mt.get_translation_matrix([0.1, 2.7, 0.1])
    m = mt.compose_matrices([t, s])
    roof_detail = copy.deepcopy(cube)
    roof_detail.apply_transformation(m)
    objects.append(roof_detail)

    s = mt.get_scale_matrix([0.5, 0.3, 4., 1])
    t = mt.get_translation_matrix([0.1, 2.7, 0])
    m = mt.compose_matrices([t, s])
    roof_detail2 = copy.deepcopy(cube)
    roof_detail2.apply_transformation(m)
    objects.append(roof_detail2)

    t = mt.get_translation_matrix([2.4, 0, 0])
    roof_detail3 = copy.deepcopy(roof_detail2)
    roof_detail3.apply_transformation(t)
    objects.append(roof_detail3)

    t = mt.get_translation_matrix([0, 0, 3.2])
    roof_detail4 = copy.deepcopy(roof_detail)
    roof_detail4.apply_transformation(t)
    objects.append(roof_detail4)


    # PAREDE ESQUERDA
    s = mt.get_scale_matrix([0.1, 3., 0.75, 1])
    wall2 = copy.deepcopy(cube)
    wall2.apply_transformation(s)
    objects.append(wall2)

    s = mt.get_scale_matrix([0.1, 3., 0.5, 1])
    t = mt.get_translation_matrix([0, 0, 1.75])
    m = mt.compose_matrices([t, s])
    wall2_1 = copy.deepcopy(cube)
    wall2_1.apply_transformation(m)
    objects.append(wall2_1)

    t = mt.get_translation_matrix([0, 0, 3.25])
    wall2_2 = copy.deepcopy(wall2)
    wall2_2.apply_transformation(t)
    objects.append(wall2_2)

    s = mt.get_scale_matrix([0.1, 1., 4., 1])
    wall2_3 = copy.deepcopy(cube)
    wall2_3.apply_transformation(s)
    objects.append(wall2_3)

    s = mt.get_scale_matrix([0.1, 0.6, 4., 1])
    t = mt.get_translation_matrix([0, 2.4, 0])
    m = mt.compose_matrices([t, s])
    wall2_4 = copy.deepcopy(cube)
    wall2_4.apply_transformation(m)
    objects.append(wall2_4)

    # PERSIANAS
    s = mt.get_scale_matrix([0.03, 0.01, 1.1, 1])
    sh = mt.get_shear_matrix('x', 'y', -45)
    t = mt.get_translation_matrix([0.15, 1.1, 0.7])
    m = mt.compose_matrices([t, sh, s])
    blind = copy.deepcopy(cube)
    blind.apply_transformation(m)
    objects.append(blind)

    t = mt.get_translation_matrix([0, 0, 1.5])
    blind1 = copy.deepcopy(blind)
    blind1.apply_transformation(t)
    objects.append(blind1)

    for x in range(1, 16):
        t = mt.get_translation_matrix([0, (x*0.08), 0])
        blind2 = copy.deepcopy(blind)
        blind3 = copy.deepcopy(blind1)
        blind2.apply_transformation(t)
        blind3.apply_transformation(t)
        objects.append(blind2)
        objects.append(blind3)


    # PAREDE DIREITA
    s = mt.get_scale_matrix([0.1, 3., 4., 1])
    t = mt.get_translation_matrix([2.9, 0, 0])
    m = mt.compose_matrices([t, s])
    wall3 = copy.deepcopy(cube)
    wall3.apply_transformation(m)
    objects.append(wall3)

    # PAREDE TRÁS
    s = mt.get_scale_matrix([3., 3., 0.1, 1])
    wall = copy.deepcopy(cube)
    wall.apply_transformation(s)
    objects.append(wall)

    # PAREDE FRENTE
    t = mt.get_translation_matrix([0, 0, 4.])
    wall4 = copy.deepcopy(wall)
    wall4.apply_transformation(t)
    objects.append(wall4)

    # PAREDE TRÁS: DETALHES
    s = mt.get_scale_matrix([0.5, 2.7, 0.3, 1])
    t = mt.get_translation_matrix([0, 0, 0.1])
    m = mt.compose_matrices([t, s])
    wall_detail = copy.deepcopy(cube)
    wall_detail.apply_transformation(m)
    objects.append(wall_detail)

    t = mt.get_translation_matrix([2.5, 0, 0])
    wall_detail2 = copy.deepcopy(wall_detail)
    wall_detail2.apply_transformation(t)
    objects.append(wall_detail2)

    s = mt.get_scale_matrix([0.5, 1., 0.3, 1])
    t = mt.get_translation_matrix([0.5, 1.7, 0.1])
    m = mt.compose_matrices([t, s])
    wall_detail3 = copy.deepcopy(cube)
    wall_detail3.apply_transformation(m)
    objects.append(wall_detail3)

    t = mt.get_translation_matrix([1.5, 0, 0])
    wall_detail4 = copy.deepcopy(wall_detail3)
    wall_detail4.apply_transformation(t)
    objects.append(wall_detail4)

    s = mt.get_scale_matrix([1., 0.06, 0.25, 1])
    t = mt.get_translation_matrix([1., 1.9, 0.1])
    m = mt.compose_matrices([t, s])
    shelf = copy.deepcopy(cube)
    shelf.apply_transformation(m)
    objects.append(shelf)

    t = mt.get_translation_matrix([0, 0.3, 0])
    shelf2 = copy.deepcopy(shelf)
    shelf2.apply_transformation(t)
    objects.append(shelf2)

    t = mt.get_translation_matrix([0, 0.3, 0])
    shelf3 = copy.deepcopy(shelf2)
    shelf3.apply_transformation(t)
    objects.append(shelf3)

    # TV
    s = mt.get_scale_matrix([1., 0.6, 0.05, 1])
    t = mt.get_translation_matrix([1., 0.8, 0.1])
    m = mt.compose_matrices([t, s])
    tv = copy.deepcopy(cube)
    tv.apply_transformation(m)
    objects.append(tv)

    s = mt.get_scale_matrix([0.06, 0.6, 0.08, 1])
    t = mt.get_translation_matrix([0.94, 0.8, 0.1])
    m = mt.compose_matrices([t, s])
    tv_detail = copy.deepcopy(cube)
    tv_detail.apply_transformation(m)
    objects.append(tv_detail)

    t = mt.get_translation_matrix([1.06, 0, 0])
    tv_detail2 = copy.deepcopy(tv_detail)
    tv_detail2.apply_transformation(t)
    objects.append(tv_detail2)

    s = mt.get_scale_matrix([1.12, 0.06, 0.08, 1])
    t = mt.get_translation_matrix([0.94, 0.74, 0.1])
    m = mt.compose_matrices([t, s])
    tv_detail3 = copy.deepcopy(cube)
    tv_detail3.apply_transformation(m)
    objects.append(tv_detail3)

    t = mt.get_translation_matrix([0, 0.66, 0])
    tv_detail4 = copy.deepcopy(tv_detail3)
    tv_detail4.apply_transformation(t)
    objects.append(tv_detail4)

    # TV RACK
    s = mt.get_scale_matrix([1.2, 0.06, 0.4, 1])
    t = mt.get_translation_matrix([0.9, 0.2, 0.1])
    m = mt.compose_matrices([t, s])
    tv_rack = copy.deepcopy(cube)
    tv_rack.apply_transformation(m)
    objects.append(tv_rack)

    t = mt.get_translation_matrix([0, 0.2, 0])
    tv_rack2 = copy.deepcopy(tv_rack)
    tv_rack2.apply_transformation(t)
    objects.append(tv_rack2)

    s = mt.get_scale_matrix([0.06, 0.4, 0.35, 1])
    t = mt.get_translation_matrix([0.95, 0, 0.1])
    m = mt.compose_matrices([t, s])
    tv_rack3 = copy.deepcopy(cube)
    tv_rack3.apply_transformation(m)
    objects.append(tv_rack3)

    t = mt.get_translation_matrix([1.04, 0, 0])
    tv_rack4 = copy.deepcopy(tv_rack3)
    tv_rack4.apply_transformation(t)
    objects.append(tv_rack4)

    # SPEAKERS
    s = mt.get_scale_matrix([0.2, 0.9, 0.3, 1])
    t = mt.get_translation_matrix([0.6, 0, 0.1])
    m = mt.compose_matrices([t, s])
    speaker = copy.deepcopy(cube)
    speaker.apply_transformation(m)
    objects.append(speaker)

    t = mt.get_translation_matrix([1.6, 0, 0])
    speaker2 = copy.deepcopy(speaker)
    speaker2.apply_transformation(t)
    objects.append(speaker2)

    s = mt.get_scale_matrix([0.6, 0.2, 0.3, 1])
    t = mt.get_translation_matrix([1.2, 0.46, 0.1])
    m = mt.compose_matrices([t, s])
    device = copy.deepcopy(cube)
    device.apply_transformation(m)
    objects.append(device)

    return objects


def main():
    d = 0.5
    window_height = 1
    window_width = 1
    pixels_height = 200
    pixels_width = 200

    objects = create_objects()

    punctual_light = PunctualLightSource(intensity=[1., 1., 1.], position=[1.5, 2.9, 2.])
    # spot_light = SpotLightSource(intensity=[0.8, 0.8, 0.8], position=[3.5, 3.5, 3.5],
    #                              direction=[0.5, 0.5, 0.5], theta=20.0)
    # infinity_light = InfinityLightSource([0.8, 0.8, 0.8], [1., 0., 1.])

    po = [1.5, 1.5, 3.5, 1.0]
    look_at = np.array([1.5, 1.5, 1.5, 1.0])
    a_vup = look_at + [0, 1, 0., 0]

    scenario = Scenario(objects=objects, light_sources=[punctual_light],
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[5/255, 154/255, 244/255],
                        ambient_light=[1., 1., 1.])

    scenario.render(window_width, window_height, d, pixels_width, pixels_height)


if __name__ == '__main__':
    main()
