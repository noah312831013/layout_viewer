import json
import numpy as np
from utils.conversion import xyz2uv
import os

def read_zind(data_dir, house_index, pano_num, layout_type):
    with open(os.path.join(data_dir, house_index, f"zind_data.json"), 'r') as f2:
        data = json.load(f2)

    merger = data['merger']
    found = 0
    for floor in merger.values():
        for complete_room in floor.values():
            for partial_room in complete_room.values():
                for pano_index in partial_room:
                    if pano_index.split('_')[-1] == pano_num:
                        pano = partial_room[pano_index]
                        found = 1
                    if found == 1:
                        break
    if found == 0:
        print("not found")
        return -1


    if layout_type not in pano:
        print("layout_type not in pano")
        return -1

    layout = pano[layout_type]
    # corners
    corner_xz = np.array(layout['vertices'])
    corner_xz[..., 0] = -corner_xz[..., 0]
    corner_xyz_f = np.insert(corner_xz, 1, pano['camera_height'], axis=1)
    corner_xyz_c = np.insert(corner_xz, 1, -(pano['ceiling_height']-pano['camera_height']), axis=1)
    corners_f = xyz2uv(corner_xyz_f).astype(np.float32)
    corners_c = xyz2uv(corner_xyz_c).astype(np.float32)
    return [corners_c, corners_f]