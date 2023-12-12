import os.path

import torch
import pickle
import gzip
from pathlib import Path
import requests
from matplotlib import pyplot
import numpy as np
import torch.nn.functional as F
from torch import nn

base_dir = "/Users/lkg/computer-vision/3：pytorch/2-3神经网络实战分类与回归任务"


class mnist_nn(nn.Module):
    def __init__(self):
        super(mnist_nn, self).__init__()
        self.hidden1 = nn.Linear(784, 128)  # Linear 线形层
        self.hidden2 = nn.Linear(128, 256)
        self.out = nn.Linear(256, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        """ forward 向前传播。反向传播 pytorch 自动完成"""
        x = F.relu(self.hidden1(x))
        x = self.dropout(x)  # 全连接层一般都需要加 dropout
        x = F.relu(self.hidden2(x))
        x = self.dropout(x)
        x = self.out(x)
        return x


def loss_batch(model, loss_func, xb, yb, opt=None):
    loss = loss_func(model(xb), yb)

    if opt is not None:
        loss.backward()
        opt.step()
        opt.zero_grad()

    return loss.item(), len(xb)


if __name__ == '__main__':
    # 1. 准备数据
    DATA_PATH = Path(os.path.join(base_dir, "data"))
    PATH = DATA_PATH / "mnist"
    PATH.mkdir(parents=True, exist_ok=True)
    URL = "http://deeplearning.net/data/mnist/"
    FILENAME = "mnist.pkl.gz"
    if not (PATH / FILENAME).exists():  # 不存在就下载
        content = requests.get(URL + FILENAME).content
        (PATH / FILENAME).open("wb").write(content)

    # 2. 打开数据
    with gzip.open((PATH / FILENAME).as_posix(), "rb") as f:
        # pickle 持续化模块：就是让数据持久化保存。
        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")
        pyplot.imshow(x_train[0].reshape((28, 28)), cmap="gray")
        print(x_train.shape)  # (50000, 784) 784 是 mnist 数据集每个样本的像素点个数
        x_train, y_train, x_valid, y_valid = map(torch.tensor, (x_train, y_train, x_valid, y_valid))
        n, c = x_train.shape
        x_train, x_train.shape, y_train.min(), y_train.max()
        print("x_train:", x_train)
        print("y_train:", y_train)
        print(x_train.shape)
        print(y_train.min(), y_train.max())
        # cross_entropy 交叉熵 交叉熵是一种用于衡量两个概率分布之间差异的度量。
        # 它常用于评估模型的预测结果与真实标签之间的差异。
        loss_func = F.cross_entropy  # 损失函数
        #
        #
        # def model(xb1):
        #     return xb1.mm(weights) + bias
        #
        #
        # bs = 64  # batch_size 一批处理的数量
        # xb = x_train[0:bs]
        # yb = y_train[0:bs]
        # print(f"xb:{xb} \nyb:{yb}")
        # weights = torch.randn([784, 10], dtype=torch.float, requires_grad=True)  # 权重，初始化随机设置
        # bias = torch.zeros(10, requires_grad=True)  # bias 偏置
        # print("loss_func(model(xb), yb) :", loss_func(model(xb), yb))

        net = mnist_nn()
        print("net:", net)
        print("net.parameters:", net.parameters())

        for name, parameter in net.named_parameters():
            print(f"name: {name}, \nparameter: {parameter}, \nparameter.size(): {parameter.size()}")

        # 使用TensorDataset和DataLoader来简化
        from torch.utils.data import TensorDataset
        from torch.utils.data import DataLoader

        bs = 64
        train_ds = TensorDataset(x_train, y_train)
        train_dl = DataLoader(train_ds, batch_size=bs, shuffle=True)

        valid_ds = TensorDataset(x_valid, y_valid)
        valid_dl = DataLoader(valid_ds, batch_size=bs * 2)


        def get_data(train_ds, valid_ds, bs):
            return (
                DataLoader(train_ds, batch_size=bs, shuffle=True),
                DataLoader(valid_ds, batch_size=bs * 2),
            )


        def fit(steps, model, loss_func, opt, train_dl, valid_dl):
            """ fit 训练函数。opt: 优化器"""
            for step in range(steps):
                model.train()  # 训练
                for xb, yb in train_dl:
                    loss_batch(model, loss_func, xb, yb, opt)

                # 训练完后：验证，评估
                model.eval()
                with torch.no_grad():
                    losses, nums = zip(*[loss_batch(model, loss_func, xb, yb) for xb, yb in valid_dl])
                val_loss = np.sum(np.multiply(losses, nums)) / np.sum(nums)
                print('当前step:' + str(step), '验证集损失：' + str(val_loss))


        from torch import optim


        def get_model():
            model = mnist_nn()
            # SGD 是一种随机梯度下降优化器，lr：学习率。
            return model, optim.SGD(model.parameters(), lr=0.001)


        def loss_batch(model, loss_func, xb, yb, optimizer=None):
            loss = loss_func(model(xb), yb)  # 计算损失函数

            if optimizer is not None:
                loss.backward()  # 反向传播
                optimizer.step()  # 更新模型参数
                optimizer.zero_grad()  # 清空之前的梯度

            return loss.item(), len(xb)


        train_dl, valid_dl = get_data(train_ds, valid_ds, bs)
        model, opt = get_model()
        fit(25, model, loss_func, opt, train_dl, valid_dl)
