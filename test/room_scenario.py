import sys
sys.path.append("..")
from ray_casting.transformations import model_transformations as mt
import copy
from ray_casting.objectModeling import obj
from ray_casting.scenario.scenario import *

def create_objects():
    cube = obj.Obj().import_obj('../objects/cube.obj')

    objects = []

    # MATERIALS

    specular_term = [1, 1, 1]
    m = 10
    # WALLS MATERIAL
    rgb_wall_material = [44/255, 137/255, 142/255]
    wall_material = obj.Material(rgb_wall_material, rgb_wall_material, specular_term, m)

    # CEILING MATERIAL
    rgb_ceiling_material = [200/255, 203/255, 208/255]
    ceiling_material = obj.Material(rgb_ceiling_material, rgb_ceiling_material, specular_term, m)

    # FLOOR MATERIAL
    floor_material = obj.Material(rgb_ceiling_material, rgb_ceiling_material, specular_term, m)

    #  BLACK MATERIAL
    rgb_black = [0, 0, 0]
    black_material = obj.Material(rgb_black, rgb_black, specular_term, m)

    # WOOD MATERIAL
    rgb_wood_dark = [89/255, 63/255, 44/255]
    rgb_wood_light = [144/255, 112/255, 100/255]
    wood_material_dark = obj.Material(rgb_wood_dark, rgb_wood_dark, specular_term, m)
    wood_material_light = obj.Material(rgb_wood_light, rgb_wood_light, specular_term, m)

    # SOFA MATERIAL
    rgb_sofa = [93/255, 83/255, 87/255]
    sofa_material = obj.Material(rgb_sofa, rgb_sofa, specular_term, m)

    rgb_gray_light = [144/255, 150/255, 169/255]
    gray_material_light = obj.Material(rgb_gray_light, rgb_gray_light, specular_term, m)

    # OBJECTS

    # CHÃO
    s = mt.get_scale_matrix([3., 0.1, 4., 1])
    floor = copy.deepcopy(cube)
    floor.apply_transformation(s)
    floor.apply_material(floor_material)
    objects.append(floor)

    # TETO
    t = mt.get_translation_matrix([0, 3., 0])
    roof = copy.deepcopy(floor)
    roof.apply_transformation(t)
    roof.apply_material(ceiling_material)
    objects.append(roof)

    # TETO: DETALHES
    s = mt.get_scale_matrix([3., 0.3, 0.8, 1])
    t = mt.get_translation_matrix([0.1, 2.7, 0.1])
    m = mt.compose_matrices([t, s])
    roof_detail = copy.deepcopy(cube)
    roof_detail.apply_transformation(m)
    roof_detail.apply_material(ceiling_material)
    objects.append(roof_detail)

    s = mt.get_scale_matrix([0.5, 0.3, 4., 1])
    t = mt.get_translation_matrix([0.1, 2.7, 0])
    m = mt.compose_matrices([t, s])
    roof_detail2 = copy.deepcopy(cube)
    roof_detail2.apply_transformation(m)
    roof_detail2.apply_material(ceiling_material)
    objects.append(roof_detail2)

    t = mt.get_translation_matrix([2.4, 0, 0])
    roof_detail3 = copy.deepcopy(roof_detail2)
    roof_detail3.apply_transformation(t)
    roof_detail3.apply_material(ceiling_material)
    objects.append(roof_detail3)

    t = mt.get_translation_matrix([0, 0, 3.2])
    roof_detail4 = copy.deepcopy(roof_detail)
    roof_detail4.apply_transformation(t)
    roof_detail4.apply_material(ceiling_material)
    objects.append(roof_detail4)

    # PAREDE ESQUERDA
    s = mt.get_scale_matrix([0.1, 3., 0.75, 1])
    wall2 = copy.deepcopy(cube)
    wall2.apply_transformation(s)
    wall2.apply_material(wall_material)
    objects.append(wall2)

    s = mt.get_scale_matrix([0.1, 3., 0.5, 1])
    t = mt.get_translation_matrix([0, 0, 1.75])
    m = mt.compose_matrices([t, s])
    wall2_1 = copy.deepcopy(cube)
    wall2_1.apply_transformation(m)
    wall2_1.apply_material(wall_material)
    objects.append(wall2_1)

    t = mt.get_translation_matrix([0, 0, 3.25])
    wall2_2 = copy.deepcopy(wall2)
    wall2_2.apply_transformation(t)
    wall2_2.apply_material(wall_material)
    objects.append(wall2_2)

    s = mt.get_scale_matrix([0.1, 1., 4., 1])
    wall2_3 = copy.deepcopy(cube)
    wall2_3.apply_transformation(s)
    wall2_3.apply_material(wall_material)
    objects.append(wall2_3)

    s = mt.get_scale_matrix([0.1, 0.6, 4., 1])
    t = mt.get_translation_matrix([0, 2.4, 0])
    m = mt.compose_matrices([t, s])
    wall2_4 = copy.deepcopy(cube)
    wall2_4.apply_transformation(m)
    wall2_4.apply_material(wall_material)
    objects.append(wall2_4)

    # PERSIANAS
    s = mt.get_scale_matrix([0.03, 0.01, 1.05, 1])
    sh = mt.get_shear_matrix('x', 'y', -45)
    t = mt.get_translation_matrix([0.15, 1.1, 0.77])
    m = mt.compose_matrices([t, sh, s])
    blind = copy.deepcopy(cube)
    blind.apply_transformation(m)
    objects.append(blind)

    t = mt.get_translation_matrix([0, 0, 1.38])
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
    wall3.apply_material(wall_material)
    objects.append(wall3)

    # PAREDE TRÁS
    s = mt.get_scale_matrix([3., 3., 0.1, 1])
    wall = copy.deepcopy(cube)
    wall.apply_transformation(s)
    wall.apply_material(wall_material)
    objects.append(wall)

    # PAREDE FRENTE
    t = mt.get_translation_matrix([0, 0, 4.])
    wall4 = copy.deepcopy(wall)
    wall4.apply_transformation(t)
    wall4.apply_material(wall_material)
    objects.append(wall4)

    # PAREDE TRÁS: DETALHES
    s = mt.get_scale_matrix([0.5, 2.7, 0.3, 1])
    t = mt.get_translation_matrix([0, 0, 0.1])
    m = mt.compose_matrices([t, s])
    wall_detail = copy.deepcopy(cube)
    wall_detail.apply_transformation(m)
    wall_detail.apply_material(wood_material_dark)
    objects.append(wall_detail)

    t = mt.get_translation_matrix([2.5, 0, 0])
    wall_detail2 = copy.deepcopy(wall_detail)
    wall_detail2.apply_transformation(t)
    wall_detail2.apply_material(wood_material_dark)
    objects.append(wall_detail2)

    s = mt.get_scale_matrix([0.5, 1., 0.3, 1])
    t = mt.get_translation_matrix([0.5, 1.7, 0.1])
    m = mt.compose_matrices([t, s])
    wall_detail3 = copy.deepcopy(cube)
    wall_detail3.apply_transformation(m)
    wall_detail3.apply_material(wood_material_dark)
    objects.append(wall_detail3)

    t = mt.get_translation_matrix([1.5, 0, 0])
    wall_detail4 = copy.deepcopy(wall_detail3)
    wall_detail4.apply_transformation(t)
    wall_detail4.apply_material(wood_material_dark)
    objects.append(wall_detail4)

    # PRATELEIRAS DA PAREDE DE TRÁS
    s = mt.get_scale_matrix([1., 0.06, 0.25, 1])
    t = mt.get_translation_matrix([1., 1.9, 0.1])
    m = mt.compose_matrices([t, s])
    shelf = copy.deepcopy(cube)
    shelf.apply_transformation(m)
    shelf.apply_material(wood_material_dark)
    objects.append(shelf)

    t = mt.get_translation_matrix([0, 0.3, 0])
    shelf2 = copy.deepcopy(shelf)
    shelf2.apply_transformation(t)
    shelf2.apply_material(wood_material_dark)
    objects.append(shelf2)

    t = mt.get_translation_matrix([0, 0.3, 0])
    shelf3 = copy.deepcopy(shelf2)
    shelf3.apply_transformation(t)
    shelf3.apply_material(wood_material_dark)
    objects.append(shelf3)

    # TV
    s = mt.get_scale_matrix([1., 0.6, 0.05, 1])
    t = mt.get_translation_matrix([1., 0.8, 0.1])
    m = mt.compose_matrices([t, s])
    tv = copy.deepcopy(cube)
    tv.apply_transformation(m)
    tv.apply_material(gray_material_light)
    objects.append(tv)

    s = mt.get_scale_matrix([0.06, 0.6, 0.08, 1])
    t = mt.get_translation_matrix([0.94, 0.8, 0.1])
    m = mt.compose_matrices([t, s])
    tv_detail = copy.deepcopy(cube)
    tv_detail.apply_transformation(m)
    tv_detail.apply_material(black_material)
    objects.append(tv_detail)

    t = mt.get_translation_matrix([1.06, 0, 0])
    tv_detail2 = copy.deepcopy(tv_detail)
    tv_detail2.apply_transformation(t)
    tv_detail2.apply_material(black_material)
    objects.append(tv_detail2)

    s = mt.get_scale_matrix([1.12, 0.06, 0.08, 1])
    t = mt.get_translation_matrix([0.94, 0.74, 0.1])
    m = mt.compose_matrices([t, s])
    tv_detail3 = copy.deepcopy(cube)
    tv_detail3.apply_transformation(m)
    tv_detail3.apply_material(black_material)
    objects.append(tv_detail3)

    t = mt.get_translation_matrix([0, 0.66, 0])
    tv_detail4 = copy.deepcopy(tv_detail3)
    tv_detail4.apply_transformation(t)
    tv_detail4.apply_material(black_material)
    objects.append(tv_detail4)

    # TV RACK
    s = mt.get_scale_matrix([1.2, 0.06, 0.4, 1])
    t = mt.get_translation_matrix([0.9, 0.2, 0.1])
    m = mt.compose_matrices([t, s])
    tv_rack = copy.deepcopy(cube)
    tv_rack.apply_transformation(m)
    tv_rack.apply_material(wood_material_light)
    objects.append(tv_rack)

    t = mt.get_translation_matrix([0, 0.2, 0])
    tv_rack2 = copy.deepcopy(tv_rack)
    tv_rack2.apply_transformation(t)
    tv_rack2.apply_material(wood_material_light)
    objects.append(tv_rack2)

    s = mt.get_scale_matrix([0.06, 0.4, 0.35, 1])
    t = mt.get_translation_matrix([0.95, 0, 0.1])
    m = mt.compose_matrices([t, s])
    tv_rack3 = copy.deepcopy(cube)
    tv_rack3.apply_transformation(m)
    tv_rack3.apply_material(wood_material_light)
    objects.append(tv_rack3)

    t = mt.get_translation_matrix([1.04, 0, 0])
    tv_rack4 = copy.deepcopy(tv_rack3)
    tv_rack4.apply_transformation(t)
    tv_rack4.apply_material(wood_material_light)
    objects.append(tv_rack4)

    # SPEAKERS
    s = mt.get_scale_matrix([0.2, 0.9, 0.3, 1])
    t = mt.get_translation_matrix([0.6, 0, 0.1])
    m = mt.compose_matrices([t, s])
    speaker = copy.deepcopy(cube)
    speaker.apply_transformation(m)
    speaker.apply_material(black_material)
    objects.append(speaker)

    t = mt.get_translation_matrix([1.6, 0, 0])
    speaker2 = copy.deepcopy(speaker)
    speaker2.apply_transformation(t)
    speaker2.apply_material(black_material)
    objects.append(speaker2)

    s = mt.get_scale_matrix([0.6, 0.2, 0.3, 1])
    t = mt.get_translation_matrix([1.2, 0.46, 0.1])
    m = mt.compose_matrices([t, s])
    device = copy.deepcopy(cube)
    device.apply_transformation(m)
    device.apply_material(black_material)
    objects.append(device)

    # SOFA 1: COSTAS
    s = mt.get_scale_matrix([0.15, 0.8, 1.5, 1])
    t = mt.get_translation_matrix([0.15, 0.1, 1.25])
    m = mt.compose_matrices([t, s])
    sofa1_1 = copy.deepcopy(cube)
    sofa1_1.apply_transformation(m)
    sofa1_1.apply_material(sofa_material)
    objects.append(sofa1_1)

    # SOFA 2: COSTAS
    t = mt.get_translation_matrix([2.55, 0, 0])
    sofa2_1 = copy.deepcopy(sofa1_1)
    sofa2_1.apply_transformation(t)
    objects.append(sofa2_1)

    # SOFA 1: BRAÇO DIREITA
    s = mt.get_scale_matrix([0.6, 0.6, 0.15, 1])
    t = mt.get_translation_matrix([0.3, 0.1, 1.25])
    m = mt.compose_matrices([t, s])
    sofa1_2 = copy.deepcopy(cube)
    sofa1_2.apply_transformation(m)
    sofa1_2.apply_material(sofa_material)
    objects.append(sofa1_2)

    # SOFA 2: BRAÇO DIREITA
    t = mt.get_translation_matrix([1.8, 0, 0])
    sofa2_2 = copy.deepcopy(sofa1_2)
    sofa2_2.apply_transformation(t)
    objects.append(sofa2_2)

    # SOFA 1: BRAÇO ESQUERDA
    t = mt.get_translation_matrix([0, 0, 1.35])
    sofa1_3 = copy.deepcopy(sofa1_2)
    sofa1_3.apply_transformation(t)
    objects.append(sofa1_3)

    # SOFA 2: BRAÇO ESQUERDA
    t = mt.get_translation_matrix([1.8, 0, 0])
    sofa2_3 = copy.deepcopy(sofa1_3)
    sofa2_3.apply_transformation(t)
    objects.append(sofa2_3)

    # SOFA 1: BASE
    s = mt.get_scale_matrix([0.6, 0.3, 1.2, 1])
    t = mt.get_translation_matrix([0.3, 0.05, 1.4])
    m = mt.compose_matrices([t, s])
    sofa1_4 = copy.deepcopy(cube)
    sofa1_4.apply_transformation(m)
    sofa1_4.apply_material(sofa_material)
    objects.append(sofa1_4)

    # SOFA 2: BASE
    t = mt.get_translation_matrix([1.8, 0, 0])
    sofa2_4 = copy.deepcopy(sofa1_4)
    sofa2_4.apply_transformation(t)
    objects.append(sofa2_4)

    # SOFA 1: ASSENTO 1
    s = mt.get_scale_matrix([0.6, 0.05, 0.60, 1])
    t = mt.get_translation_matrix([0.3, 0.35, 1.37])
    m = mt.compose_matrices([t, s])
    sofa1_5 = copy.deepcopy(cube)
    sofa1_5.apply_transformation(m)
    sofa1_5.apply_material(sofa_material)
    objects.append(sofa1_5)

    # SOFA 2: ASSENTO 1
    t = mt.get_translation_matrix([1.8, 0, 0])
    sofa2_5 = copy.deepcopy(sofa1_5)
    sofa2_5.apply_transformation(t)
    objects.append(sofa2_5)

    # SOFA 1: ASSENTO 2
    t = mt.get_translation_matrix([0, 0, 0.63])
    sofa1_6 = copy.deepcopy(sofa1_5)
    sofa1_6.apply_transformation(t)
    objects.append(sofa1_6)

    # SOFA 2: ASSENTO 2
    t = mt.get_translation_matrix([1.8, 0, 0])
    sofa2_6 = copy.deepcopy(sofa1_6)
    sofa2_6.apply_transformation(t)
    objects.append(sofa2_6)

    # MESA DE CENTRO
    s = mt.get_scale_matrix([0.6, 0.1, 1, 1])
    t = mt.get_translation_matrix([1.2, 0.3, 1.5])
    m = mt.compose_matrices([t, s])
    table1 = copy.deepcopy(cube)
    table1.apply_material(wood_material_light)
    table1.apply_transformation(m)
    objects.append(table1)

    s = mt.get_scale_matrix([0.5, 0.1, 0.2, 1])
    t = mt.get_translation_matrix([1.25, 0.1, 1.6])
    m = mt.compose_matrices([t, s])
    table2 = copy.deepcopy(cube)
    table2.apply_material(wood_material_light)
    table2.apply_transformation(m)
    objects.append(table2)

    t = mt.get_translation_matrix([0, 0, 0.6])
    table3 = copy.deepcopy(table2)
    table3.apply_transformation(t)
    objects.append(table3)


    # print total number of faces
    # size = 0
    # for obje in objects:
    #     size += len(obje.faces)
    # print(size)

    return objects


def main():
    d = 0.5
    window_height = 1
    window_width = 1

    pixels_height = 200
    pixels_width = 200

    objects = create_objects()

    punctual_light = PunctualLightSource(intensity=[0.5, 0.5, 0.5], position=[1.5, 2.9, 2.])
    spot_light = SpotLightSource(intensity=[0.5, 0.5, 0.5], position=[1.5, 2.9, 2.], direction=[0, -1, 0], theta=15)

    lights = [punctual_light, spot_light]

    po = [1.5, 1.5, 4.0, 1.0]
    look_at = np.array([1.5, 1.5, 0.0, 1.0])
    a_vup = look_at + [0, 1, 0., 0]

    p = "PERSPECTIVE"
    ob = "OBLIQUE"
    cb = "CABINET"
    cv = "CAVALIER"
    ort = "ORTHOGRAPHIC"

    projection_type = p

    scenario = Scenario(objects=objects, light_sources=lights,
                        po=po, look_at=look_at, a_vup=a_vup, background_color=[5/255, 154/255, 244/255],
                        ambient_light=[0.5, 0.5, 0.5])

    window = Window(window_width, window_height, d, pixels_width, pixels_height)

    scenario.render(window=window, ray_mean=True, parallel=False, shadow=True, projection_type=projection_type,
                    oblique_angle=0, oblique_factor=0)


if __name__ == '__main__':
    main()
