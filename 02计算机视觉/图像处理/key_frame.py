import time

import cv2


def cv_keyFrame():
    start = time.time()
    video = cv2.VideoCapture('./data/8-1.mp4')  # 读入视频文件
    print('帧速:', video.get(cv2.CAP_PROP_FPS))
    print('总帧数:', video.get(cv2.CAP_PROP_FRAME_COUNT))
    times = 0
    outpath = './outpath/'
    if video.isOpened():
        print("open")
    while True:
        res, image = video.read()
        if not res:
            print('not res , not image')
            break
        times += 1
        cv2.imwrite(outpath + str(times) + '.jpg', image)
        print(outpath + str(times) + '.jpg')
    print('图片提取结束')
    video.release()
    print("用时:{}s".format(int(time.time() - start)))
