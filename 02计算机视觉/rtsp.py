import cv2
import threading
import subprocess
import os

def check_rtsp_stream(url, timeout=3):
    capture = cv2.VideoCapture(url)
    success = [False]

    def open_stream():
        success[0] = capture.isOpened()

    thread = threading.Thread(target=open_stream)
    thread.start()
    thread.join(timeout)  # 等待线程，限制时间

    # 释放资源
    capture.release()
    return success[0]


def ping_ip(ip, timeout=1):
    try:
        # 使用不同的命令参数根据平台选择命令
        command = ['ping', '-c', '1', '-W', str(timeout), ip] if os.name != 'nt' else ['ping', '-n', '1', '-w', str(timeout * 1000), ip]

        # 执行命令
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 检查返回码
        if result.returncode == 0:
            # print(f"{ip} is reachable")
            return True
        else:
            # print(f"{ip} is not reachable")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


if __name__ == '__main__':
    for i in range (0, 256):
        ip = "" + str(i)
        # if ip in m:
        #     print(ip, "continue")
        #     continue
        ok = ping_ip(ip)
        if not ok:
            print(ip, "is not reachable")
            continue
        # 替换为你的 RTSP URL
        rtsp_url = f"rtsp://username:password@{ip}"
        ok = check_rtsp_stream(rtsp_url)
        if ok:
            print(rtsp_url, "ok")
        else:
            print(ip, "Couldn't read")

