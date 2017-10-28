import numpy as np


def get_world_camera_matrix(po, look_at, avup):
    ic, jc, kc = get_ijk(po, look_at, avup)

    # Appending the last column for the W->C Matrix
    i_wc = np.append(ic, -np.dot(ic, po[:3]))
    j_wc = np.append(jc, -np.dot(jc, po[:3]))
    k_wc = np.append(kc, -np.dot(kc, po[:3]))
    last_row = np.array([0, 0, 0, 1])
    
    # Stacking arrays as rows for the W->C Matrix
    world_camera_matrix = np.vstack([i_wc, j_wc, k_wc, last_row])

    return world_camera_matrix


def get_camera_world_matrix(po, look_at, avup):
    ic, jc, kc = get_ijk(po, look_at, avup)
    
    # Appending the last row [0 0 0 1] for the C->W Matrix
    i_cw = np.append(ic, 0)
    j_cw = np.append(jc, 0)
    k_cw = np.append(kc, 0)
    po_cw = np.append(po, 1)

    # Stacking arrays as columns for the C->W Matrix
    camera_world_matrix = np.column_stack((i_cw, j_cw, k_cw, po_cw))

    return camera_world_matrix


def get_ijk(po, look_at, a_vup):
    # Calculating ic, jc, and kc
    po = np.array(po[:3])
    look_at = np.array(look_at[:3])
    a_vup = np.array(a_vup[:3])
    k = po - look_at
    kc = (k / np.linalg.norm(k))
    vup = a_vup - po
    i = np.cross(vup, kc)
    ic = (i / np.linalg.norm(i))
    jc = np.cross(kc, ic)

    return ic, jc, kc


def main():
    po = np.array([1, 1, 2])
    look_at = np.array([6, 8, 0])
    avup = np.array([4, 5, 3])
    wc = get_world_camera_matrix(po, look_at, avup)
    cw = get_camera_world_matrix(po, look_at, avup)
    print(cw, "\n\n", wc)


if __name__ == '__main__':
   main()
