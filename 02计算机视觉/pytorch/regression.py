import os.path

import torch
import pickle
import gzip
from pathlib import Path
import requests
from matplotlib import pyplot
import numpy as np

base_dir = "/Users/lkg/code/vscode/technology/20jupyterLab/第三章：pytorch/第二、三章：神经网络实战分类与回归任务"

DATA_PATH = Path(os.path.join(base_dir, "data"))
PATH = DATA_PATH / "mnist"

PATH.mkdir(parents=True, exist_ok=True)

URL = "http://deeplearning.net/data/mnist/"
FILENAME = "mnist.pkl.gz"

if not (PATH / FILENAME).exists():
    content = requests.get(URL + FILENAME).content
    (PATH / FILENAME).open("wb").write(content)

if __name__ == '__main__':
    with gzip.open((PATH / FILENAME).as_posix(), "rb") as f:
        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")
        pyplot.imshow(x_train[0].reshape((28, 28)), cmap="gray")
        print(x_train.shape)  # (50000, 784) 784 是 mnist 数据集每个样本的像素点个数
        x_train, y_train, x_valid, y_valid = map(
            torch.tensor, (x_train, y_train, x_valid, y_valid)
        )
        n, c = x_train.shape
        x_train, x_train.shape, y_train.min(), y_train.max()
        print(x_train, y_train)
        print(x_train.shape)
        print(y_train.min(), y_train.max())
