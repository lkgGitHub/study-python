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


def boundary_fill():
    img = cv2.imread(os.path.join(base_dir, "lenaNoise.png"))
    # 边界填充
    top_size, bottom_size, left_size, right_size = (50, 50, 50, 50)
    cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, borderType=cv2.BORDER_REPLICATE)
    plt.subplots(231)


def show_image(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_smoothing():
    """图像平滑"""
    img = cv2.imread(os.path.join(base_dir, "lenaNoise.png"))
    show_image("image", img)
    # 1. 均值滤波，简单的平均卷积操作
    blur = cv2.blur(img, (3, 3))
    show_image("blur", blur)
    # 2. 方框滤波，基本和均值一样，可以选择归一化
    box = cv2.boxFilter(img, -1, (3, 3), normalize=True)
    show_image("box", box)
    # 3. 高斯滤波，高斯模糊的卷积核里的数值是满足高斯分布，相当于更重视中间的
    gaussian = cv2.GaussianBlur(img, (5, 5), 1)
    show_image('gaussian', gaussian)
    # 4. 中值滤波，相当于用中值代替
    median = cv2.medianBlur(img, 5)  # 中值滤波
    show_image('median', median)
    # 展示所有的
    res = np.hstack((blur, box, gaussian, median))
    show_image("all", res)


def erode():
    """erode(形态学)-腐蚀操作"""
    img = cv2.imread(os.path.join(base_dir, "dige.png"))
    show_image("img", img)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=3)
    show_image("erosion", erosion)
    pie = cv2.imread(os.path.join(base_dir, "pie.png"))
    kernel = np.ones((30, 30), np.uint8)
    erosion_1 = cv2.erode(pie, kernel, iterations=1)
    erosion_2 = cv2.erode(pie, kernel, iterations=2)
    erosion_3 = cv2.erode(pie, kernel, iterations=3)
    res = np.hstack((erosion_1, erosion_2, erosion_3))
    show_image("res", res)


def dilate_morphology():
    """dilate(膨胀)-形态学"""
    img = cv2.imread(os.path.join(base_dir, "dige.png"))
    show_image("img", img)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(img, kernel, iterations=3)
    show_image("dilate", dilate)
    pie = cv2.imread(os.path.join(base_dir, "pie.png"))
    kernel = np.ones((30, 30), np.uint8)
    dilate_1 = cv2.dilate(pie, kernel, iterations=1)
    dilate_2 = cv2.dilate(pie, kernel, iterations=2)
    dilate_3 = cv2.dilate(pie, kernel, iterations=3)
    res = np.hstack((dilate_1, dilate_2, dilate_3))
    show_image("res", res)


def morphology():
    """morphology(形态学)开运算与闭运算 """
    img = cv2.imread(os.path.join(base_dir, "dige.png"))
    kernel = np.ones((5, 5), np.uint8)
    # 开：先腐蚀，再膨胀
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # 闭：先膨胀，再腐蚀
    show_image("opening", opening)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    show_image("closing", closing)


def gradient_morphology():
    """ 剃度运算 """
    pie = cv2.imread(os.path.join(base_dir, 'pie.png'))
    kernel = np.ones((7, 7), np.uint8)
    dilate = cv2.dilate(pie, kernel, iterations=5)  # 膨胀
    erosion = cv2.erode(pie, kernel, iterations=5)  # 腐蚀
    res = np.hstack((dilate, erosion))
    show_image("res", res)
    # 梯度 = 膨胀 - 腐蚀
    gradient = cv2.morphologyEx(pie, cv2.MORPH_GRADIENT, kernel)
    show_image("gradient", gradient)


def hat():
    """ 礼帽与黑帽
            礼帽 = 原始输入-开运算结果
            黑帽 = 闭运算-原始输入
    """
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.imread(os.path.join(base_dir, 'dige.png'))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)  # 礼帽
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)  # 黑帽
    show_image("tophat", tophat)
    show_image("blackhat", blackhat)


def sobel():
    """dst = cv2.Sobel(src, ddepth, dx, dy, ksize)
            ddepth:图像的深度
            dx和dy分别表示水平和竖直方向
            ksize是Sobel算子的大小
        用途：表示出图像的轮廓
    """
    img = cv2.imread(os.path.join(base_dir, 'pie.png'), cv2.IMREAD_GRAYSCALE)
    show_image("img", img)
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    show_image("sobel_x", sobel_x)
    sobel_x = cv2.convertScaleAbs(sobel_x)
    show_image("sobel_x", sobel_x)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    # 白到黑是正数，黑到白就是负数了，所有的负数会被截断成0，所以要取绝对值
    sobel_y = cv2.convertScaleAbs(sobel_y)
    show_image("sobel_y", sobel_y)
    # 分别计算x和y，再求和
    sobel_x_y = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    show_image("sobel_x_y", sobel_x_y)
    # 不建议直接同时计算 x 和 y，可能效果不太好
    sobel_x_y = cv2.Sobel(img, cv2.CV_64F, 1, 1, ksize=3)
    sobel_x_y = cv2.convertScaleAbs(sobel_x_y)
    show_image('sobel_x_y2', sobel_x_y)
    # 示例：表示出图像的轮廓
    img = cv2.imread(os.path.join(base_dir, 'lena.jpg'), cv2.IMREAD_GRAYSCALE)
    show_image("lena", img)
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    sobel_x_y = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    show_image('lena_sobel_x_y', sobel_x_y)


def diff_sobel():
    """不同算子的差异"""
    img = cv2.imread(os.path.join(base_dir, 'lena.jpg'), cv2.IMREAD_GRAYSCALE)

    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    sobel_xy = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    scharr_x = cv2.Scharr(img, cv2.CV_64F, 1, 0)
    scharr_y = cv2.Scharr(img, cv2.CV_64F, 0, 1)
    scharr_x = cv2.convertScaleAbs(scharr_x)
    scharr_y = cv2.convertScaleAbs(scharr_y)
    scharr_xy = cv2.addWeighted(scharr_x, 0.5, scharr_y, 0.5, 0)

    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)

    res = np.hstack((sobel_xy, scharr_xy, laplacian))
    show_image("lena", img)
    show_image('res', res)
    show_image("lena", img)


if __name__ == "__main__":
    diff_sobel()
