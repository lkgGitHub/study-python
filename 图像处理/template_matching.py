import os

import cv2
import numpy as np

file_types = ['add_user', 'chrome', 'modify_path', 'remote_connection', 'remote_desktop_connection']  #

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


def matchTemplate(file_type, threshold, template_paths):
    boo = False
    file_dir = './data/' + file_type
    print("file_dir", file_dir)
    for f in os.listdir(file_dir):
        img_path = file_dir + '/' + f
        img_rgb = cv2.imread(img_path)
        img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        for template_path in template_paths:
            template = cv2.imread('template/{}.jpg'.format(template_path), 0)
            w, h = template.shape[::-1]

            # Apply template Matching
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            print("{}:({}, {})".format(f, loc[0].size, loc[1].size))
            if loc[0].size and loc[1].size:
                boo = True
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imshow(img_path, img_rgb)
        cv2.waitKey(0)
        print(boo)


if __name__ == '__main__':
    file_types = ['del_file', 'add_user', 'chrome', 'modify_path', 'remote_connection', 'remote_desktop_connection']  #
    matchTemplate('del_file', 0.9, ['del_file'])
    matchTemplate('modify_path', 0.9, ['modify_path'])
    matchTemplate('add_user', 0.9, ['add_user'])
    matchTemplate('remote_desktop_connection', 0.9, ['remote_desktop_connection'])
    matchTemplate('chrome', 0.9, ['chrome'])
    matchTemplate('remote_connection', 0.9, ['remote_connection'])
    matchTemplate('create_file', 0.9, ['create_file'])
    matchTemplate('into_system_disk', 0.9, ['into_system_disk'])
    matchTemplate('login_bastion', 0.9, ['login_bastion'])

    matchTemplate('uninstall_app', 0.9, ['uninstall_app1', 'uninstall_app3', 'uninstall_app4'])

# def matchTemplate(file_type, threshold):
#     template = cv2.imread('template/{}.jpg'.format(file_type), 0)
#     w, h = template.shape[::-1]
#
#     file_dir = './data/' + file_type
#     print("file_dir", file_dir)
#     for f in os.listdir(file_dir):
#         img_path = file_dir + '/' + f
#         img_rgb = cv2.imread(img_path)
#         img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#         # Apply template Matching
#         res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(res >= threshold)
#         print("{}:({}, {})".format(f, loc[0].size, loc[1].size))
#         for pt in zip(*loc[::-1]):
#             cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#         cv2.imshow(img_path, img_rgb)
#         cv2.waitKey(0)
