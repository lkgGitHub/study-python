import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
file_types = ['add_user']  # 'chrome', 'modify_path', 'remote_connection', 'remote_desktop_connection'

print('template_type', 'correct', 'error', 'total_count', sep='\t')
template_type = 'add_user'
total_count = 0
correct = 0
error = 0
# file_type = 'add_user'
template_path = './template/{}.jpg'.format(template_type)
# cv2.IMREAD_COLOR(1)：它指定加载彩色图像。图像的任何透明度都将被忽略（默认值）;
# cv2.IMREAD_GRAYSCALE(0)：它指定以灰度模式加载图像；cv2.IMREAD_UNCHANGED(-1)：它指定加载图像，包括alpha通道。
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]  # 记录图像模板的尺寸

for file_type in file_types:
    file_dir = './data/' + file_type
    for f in os.listdir(file_dir):
        total_count += 1
        img_path = file_dir + '/' + f
        img = cv2.imread(img_path, 0)
        if img is None:
            print(img_path)
            continue

        # 2.标准相关模板匹配
        try:
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
            threshold = 0.9  # 设定阈值
            loc = np.where(res >= threshold)
            if len(loc[0]) is not 0:
                if template_type in img_path:
                    correct += 1
                else:
                    error += 1
            else:
                if template_type in img_path:
                    error += 1
        except cv2.error as e:
            print(e.msg)
print(template_type, correct, error, total_count, sep='\t')

