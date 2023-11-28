import os.path

# pip3 install opencv-python opencv-contrib-python matplotlib
import cv2
import matplotlib.pyplot as plt
import numpy as np

base_dir = "/Users/lkg/Downloads/计算机视觉/第一章：Opencv/opencv计算机视觉实战/图像操作"


def cv_show(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_image(name, img):
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


def canny():
    """ Canny边缘检测
           使用高斯滤波器，以平滑图像，滤除噪声。
           计算图像中每个像素点的梯度强度和方向。
           应用非极大值（Non-Maximum Suppression）抑制，以消除边缘检测带来的杂散响应。
           应用双阈值（Double-Threshold）检测来确定真实的和潜在的边缘。
           通过抑制孤立的弱边缘最终完成边缘检测。
    """
    img = cv2.imread(os.path.join(base_dir, 'lena.jpg'), cv2.IMREAD_GRAYSCALE)
    v1 = cv2.Canny(img, 80, 250)
    v2 = cv2.Canny(img, 50, 100)
    res = np.hstack((v1, img, v2))
    show_image("res", res)

    img = cv2.imread(os.path.join(base_dir, "car.png"), cv2.IMREAD_GRAYSCALE)
    v1 = cv2.Canny(img, 120, 250)
    v2 = cv2.Canny(img, 50, 100)
    res = np.hstack((v1, img, v2))
    show_image("res", res)


def pyramid():
    """ 图像金字塔¶
            高斯金字塔
            拉普拉斯金字塔
    """
    img = cv2.imread(os.path.join(base_dir, 'AM.png'))
    show_image("img", img)
    print(img.shape)

    up = cv2.pyrUp(img)
    show_image("up", up)
    print(up.shape)

    down = cv2.pyrDown(img)
    show_image("down", down)
    print(down.shape)

    up = cv2.pyrUp(img)
    up_down = cv2.pyrDown(up)
    show_image('img,up_down', np.hstack((img, up_down)))

    # 拉普拉斯金字塔
    up = cv2.pyrUp(img)
    up_down = cv2.pyrDown(up)
    show_image('img-up_down', img - up_down)


def find_contours():
    """cv2.findContours(img,mode,method)
        mode:轮廓检索模式
            - RETR_EXTERNAL ：只检索最外面的轮廓；
            - RETR_LIST：检索所有的轮廓，并将其保存到一条链表当中；
            - RETR_CCOMP：检索所有的轮廓，并将他们组织为两层：顶层是各部分的外部边界，第二层是空洞的边界;
            - RETR_TREE：检索所有的轮廓，并重构嵌套轮廓的整个层次;

        method:轮廓逼近方法
            - CHAIN_APPROX_NONE：以Freeman链码的方式输出轮廓，所有其他方法输出多边形（顶点的序列）。
            - CHAIN_APPROX_SIMPLE:压缩水平的、垂直的和斜的部分，也就是，函数只保留他们的终点部分。

        使用 cv2.findContours() 的基本步骤：
            将图像转换为灰度图像。
            对灰度图像进行二值化处理。
            使用 cv2.findContours() 查找轮廓。
            使用 cv2.drawContours() 绘制轮廓。

    """
    img = cv2.imread(os.path.join(base_dir, 'contours.png'))
    cv_show(img, "contours")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度图
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv_show(thresh, "thresh")
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 传入绘制图像，轮廓，轮廓索引，颜色模式，线条厚度
    # 注意需要copy,要不原图会变。。
    draw_img = img.copy()
    res = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)
    cv_show(res, "drawContours")
    draw_img = img.copy()
    res = cv2.drawContours(draw_img, contours, 2, (0, 0, 255), 2)
    cv_show(res, 'drawContours2')

    # 轮廓特征
    cnt = contours[0]
    print("面积：", cv2.contourArea(cnt))  # 面积
    print("周长：", cv2.arcLength(cnt, True))  # 周长，True 表示闭合的

    # 轮廓近似
    img = cv2.imread(os.path.join(base_dir, 'contours2.png'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    draw_img = img.copy()
    res = cv2.drawContours(draw_img, [cnt], -1, (0, 0.255), 2)
    cv_show(res, 'res')
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    draw_img = img.copy()
    res = cv2.drawContours(draw_img, [approx], -1, (0, 0, 255), 2)
    cv_show(res, "approx")

    # 边界矩形
    img = cv2.imread(os.path.join(base_dir, 'contours.png'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv_show(img, "rect")

    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    rect_area = w * h
    extent = float(area) / rect_area
    print('轮廓面积与边界矩形比', extent)

    # 外接圆
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)
    circle = cv2.circle(img, center, radius, (0, 255, 0), 2)
    cv_show(circle, "circle")


if __name__ == "__main__":
    find_contours()
