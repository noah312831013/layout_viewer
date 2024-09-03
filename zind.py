import os
from dataset.read_zind import read_zind
from visualization.boundary import draw_boundaries
import cv2

class zind():
    def __init__(self, root):
        self.root = root
        self.house_list = sorted(os.listdir(root))
    def get_pano_list(self, house):
        pano_list = sorted([pano.replace('.jpg', '') for pano in os.listdir(self.root + '/' + house+'/'+"panos")])
        return pano_list
    def visualize(self, house, pano, layout_type):
        pano_num = pano.split('_')[-1]
        pano_img_path = os.path.join(self.root, house, "panos",pano + '.jpg')
        pano_img = cv2.imread(pano_img_path)
        pano_img = cv2.cvtColor(pano_img, cv2.COLOR_BGR2RGB)
        corners_list = read_zind(self.root, house, pano_num, layout_type)
        return draw_boundaries(pano_img,corners_list)

