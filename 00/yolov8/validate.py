from ultralytics import YOLO
import os

# fix: OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
# 原因：conflicting installations in numpy and from canopy.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def validate():
    """验证"""
    # Load a model
    model = YOLO('yolov8n.pt')  # load an official model
    model = YOLO('path/to/best.pt')  # load a custom model

    # Validate the model
    metrics = model.val()  # no arguments needed, dataset and settings remembered
    metrics.box.map  # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps  # a list contains map50-95 of each category
