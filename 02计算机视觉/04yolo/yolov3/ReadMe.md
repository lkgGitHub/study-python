# 训练 YOLOv3

# 1. 准备数据

标注数据，标注工具 labelme

https://github.com/labelmeai/labelme
`pip install labelme`

# 2. 写好模型所需的配置文件

`bash create_custom_model.sh 2`
脚本生成 yolo3-custom.cfg

# 3. 数据预处理

标签格式转换。YOLOv3 使用的是 x, y, wide, height，即中心点和长宽，相对位置(0~1)
写好数据和标签路径
