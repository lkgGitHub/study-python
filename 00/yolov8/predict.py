from ultralytics import YOLO
import os

# fix: OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
# 原因：conflicting installations in numpy and from canopy.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def predict():
    # Load a model
    model = YOLO('yolov8n.pt')  # load an official model

    # Predict with the model
    results = model('https://ultralytics.com/images/bus.jpg')
