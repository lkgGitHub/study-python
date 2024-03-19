import os

import cv2

image_path = ''
label_path = ''


def cv_show(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def relative_to_absolute(img, relative_coord):
    """
    将图片的相对坐标转换为绝对坐标。

    Args:
      img: 输入图像。
      relative_coord: 相对坐标，格式为 (x, y)。

    Returns:
      绝对坐标，格式为 (x, y)。
    """

    img_h, img_w = img.shape[:2]
    x = int(relative_coord[0] * img_w)
    y = int(relative_coord[1] * img_h)
    return x, y


if __name__ == '__main__':
    for label_file in os.listdir(label_path):
        p = os.path.join(label_path, label_file)
        with open(p, 'r') as f:
            for line in f:
                cols = line.split()
                filename, ext = os.path.splitext(label_file)
                ima_path = os.path.join(image_path, filename + ".jpg")
                img = cv2.imread(ima_path)
                top_left_corner = relative_to_absolute(img, (float(cols[1]), float(cols[2])))
                bottom_right_corner = relative_to_absolute(img, (float(cols[3]), float(cols[4])))
                cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 255, 0), 2)
                cv_show(img, label_file)
