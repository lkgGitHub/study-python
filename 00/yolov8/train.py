from ultralytics import YOLO
import os

# fix: OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
# 原因：conflicting installations in numpy and from canopy.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def train():
    """训练"""
    # 加载模型
    model = YOLO("yolov8n.pt")  # 加载预训练模型（建议用于训练）

    # 训练模型。epoch 迭代次数
    results = model.train(data='coco128.yaml', epochs=20, imgsz=640)


if __name__ == '__main__':
    train()
