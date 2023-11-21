import os.path

# pip3 install opencv-python opencv-contrib-python matplotlib
import cv2
import matplotlib.pyplot as plt
import numpy as np

base_dir = "/Users/lkg/Downloads/计算机视觉/第一章：Opencv/opencv计算机视觉实战/图像操作"


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def read_image():
    #  cv2.IMREAD_GRAYSCALE 灰度图
    img = cv2.imread(os.path.join(base_dir, "cat.jpg"), cv2.IMREAD_GRAYSCALE)
    print("img.shape:", img.shape)
    print("type(img):", type(img))
    print("img.size:", img.size)
    print("img.dtype:", img.dtype)
    print("img:", img)
    # 截取部分图像数据
    cat = img[0:200, 0:200]
    cv_show('cat', cat)


def read_video():
    # 读取视频
    vc = cv2.VideoCapture(os.path.join(base_dir, "test.mp4"))
    # 检查是否打开正确
    opened = vc.isOpened()

    while opened:
        opened, frame = vc.read()
        if frame is None:
            break
        if opened:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('result', gray)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    vc.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = cv2.imread(os.path.join(base_dir, "cat.jpg"))
    # 边界填充
    top_size, bottom_size, left_size, right_size = (50, 50, 50, 50)
    cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, borderType=cv2.BORDER_REPLICATE)
    plt.subplots(231)
