import cv2


def show_image():
    # 读取图像
    img = cv2.imread('Pictures/custom/fire.jpeg')

    # 定义矩形框的左上角和右下角坐标
    start_point = (553, 198)
    end_point = (620, 257)

    # 定义矩形框的颜色 (B, G, R) 和线条粗细
    color = (0, 255, 0)  # 绿色
    thickness = 2

    # 在图像上绘制矩形框
    cv2.rectangle(img, start_point, end_point, color, thickness)

    # 显示图像
    cv2.imshow('Image with Rectangle', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def positions_to_point(x, y, width, height):
    tl = (x, y)  # top - left 左上角点的坐标
    br = (x + width, y + height)  # bottom - right  右下角点的坐标
    print(tl, br)
    return tl, br


def point_to_positions(tr, br):
    x = tr[0]
    y = tr[1]
    width = br[0] - x
    height = br[1] - y
    print(f'"x": {x}, "y": {y}, "width": {width}, "height": {height}')


# positions
if __name__ == '__main__':
    show_image()
