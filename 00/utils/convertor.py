import json
import os
import shutil
from os import path

import cv2


def read_json_file(filename):
    """
    按行读取文件，并把每行字符串转为 JSON

    Args:
      filename: 文件名

    Returns:
      一个列表，包含每个行的 JSON 对象
    """

    with open(filename, 'r') as f:
        f_lines = f.readlines()

    json_objects = []
    for line in f_lines:
        json_object = json.loads(line)
        json_objects.append(json_object)

    return json_objects


def cv_show(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def absolute_to_relative(img, absolute_coord):
    """
    将图片的相对坐标转换为绝对坐标。

    Args:
      img: 输入图像。
      absolute_coord: 相对坐标，格式为 (x, y)。

    Returns:
      绝对坐标，格式为 (x, y)。
    """

    img_h, img_w = img.shape[:2]
    x = float(absolute_coord[0] / img_w)
    y = float(absolute_coord[1] / img_h)
    return x, y


if __name__ == '__main__':
    lines2 = read_json_file(original_data)
    for line in lines2:
        results = line["result"]["result"]
        for result in results:
            if len(result['data']) > 0:
                img = cv2.imread(path.join(image_base_path, line["result"]['image']))
                # cv2.rectangle(img, (int(result['data'][0]), int(result['data'][1])),
                #               (int(result['data'][2]), int(result['data'][3])),
                #               (255, 0, 0), 3)
                # cv_show(img, line["result"]['image'])
                filename = os.path.basename(line["result"]['image'])
                src_path = path.join(image_base_path, line["result"]['image'])
                dst_path = path.join(dst_dir, "images", filename)
                shutil.copy(src_path, dst_path)

                x1, y1 = absolute_to_relative(img, (int(result['data'][0]), int(result['data'][1])))
                x2, y2 = absolute_to_relative(img, (int(result['data'][2]), int(result['data'][3])))
                fn, ext = os.path.splitext(filename)
                label_path = path.join(dst_dir, "labels", fn + ".txt")
                with open(label_path, "w") as f:
                    f.write(f"1 {x1} {y1} {x2} {y2} \n")
