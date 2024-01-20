import argparse
import os

from utils.logger import Logger
from utils.parse_config import *
from utils.utils import *

import torch

base_path = os.getcwd()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100, help="number of epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="size of each image batch")
    parser.add_argument("--gradient_accumulations", type=int, default=2, help="number of gradient accums before step")
    parser.add_argument("--model_def", type=str, default="config/yolov3.cfg", help="path to model definition file")
    parser.add_argument("--data_config", type=str, default="config/coco.data", help="path to data config file")
    parser.add_argument("--pretrained_weights", type=str, help="if specified starts from checkpoint model")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    parser.add_argument("--checkpoint_interval", type=int, default=1, help="interval between saving model weights")
    parser.add_argument("--evaluation_interval", type=int, default=1, help="interval evaluations on validation set")
    parser.add_argument("--compute_map", default=False, help="if True computes mAP every tenth batch")
    parser.add_argument("--multiscale_training", default=True, help="allow for multi-scale training")
    opt = parser.parse_args()
    print("启动参数")
    # vars() 是 Python 内置函数之一，用于返回对象的属性和属性值的字典形式
    for arg in vars(opt):
        print(arg, ":", getattr(opt, arg))

    logger = Logger("logs")
    # device = torch.device("cuda" if torch.cuda.is_available() else "")

    os.makedirs("output", exist_ok=True)  # exist_ok=True 不抛出异常
    os.makedirs("checkpoints", exist_ok=True)

    data_config = parse_data_config(opt.data_config)
    print("data_config:", data_config)
    for key, value in data_config.items():
        print(f'{key}: {value}')

    train_path = data_config["train"]
    valid_path = data_config["valid"]

    class_names = load_classes(os.path.join(base_path, data_config["names"]))
    print("class_names:", class_names)
    for i, n in enumerate(class_names):
        print(f'{i}: {n}')

    # Initiate model 初始化模型
