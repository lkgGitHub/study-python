from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model

# Export the model
model.export(format='onnx')
# model.export(format='engine')

# ONNX (Open Neural Network Exchange) 开放神经网络交换
# 是一种针对机器学习模型而设计的开放文件格式，用于存储训练好的模型。

# 格式	    format  模型文件	        元数据	论据
# ONNX	    onnx	yolov8n.onnx	✅	    imgsz, half, dynamic, simplify, opset
# TensorRT	engine	yolov8n.engine	✅	    imgsz, half, dynamic, simplify, workspace
