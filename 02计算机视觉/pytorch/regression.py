import datetime
import os.path

import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt
from sklearn import preprocessing

base_dir = "/Users/lkg/computer-vision/3：pytorch/2-3神经网络实战分类与回归任务"

if __name__ == '__main__':
    features = pd.read_csv(os.path.join(base_dir, "temps.csv"))
    print(features.head(3))
    print("数据维度", features.shape)  # (348, 9)，即 348 行，9列
    years = features['year']
    months = features['month']
    days = features['day']
    dates = [f'{year}-{month}-{day}' for year, month, day in zip(years, months, days)]
    dates = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in dates]
    print(dates[0:5])
    plt.style.use('fivethirtyeight')

    # 设置布局
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    fig.autofmt_xdate(rotation=45)  # rotation=45, 旋转 45 度

    # 标签值
    ax1.plot(dates, features['actual'])
    ax1.set_xlabel('')
    ax1.set_ylabel('Temperature')
    ax1.set_title('actual Max Temp')

    # 昨天
    ax2.plot(dates, features['temp_1'])
    ax2.set_xlabel('')
    ax2.set_ylabel('Temperature')
    ax2.set_title('Previous Max Temp')

    # 前天
    ax3.plot(dates, features['temp_2'])
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Temperature')
    ax3.set_title('Two Days Prior Max Temp')

    # 我的逗逼朋友
    ax4.plot(dates, features['friend'])
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Temperature')

    plt.tight_layout(pad=2)
    # plt.show()  # 语句用于显示绘制的图像

    # 独热编码，get_dummies: 将离散型特征的每一种取值都看成一种状态
    features = pd.get_dummies(features)
    print("features.head(5):\n", features.head(5))

    # 标签
    labels = np.array(features['actual'])

    # 在特征中去掉标签
    features = features.drop('actual', axis=1)

    # 名字单独保存有一下
    feature_header = list(features.columns)
    print("feature_header:", feature_header)

    features = np.array(features)

    # 标准化处理
    input_features = preprocessing.StandardScaler().fit_transform(features)

    # 构建网络模型
    x = torch.tensor(input_features, dtype=float)
    y = torch.tensor(labels, dtype=float)

    print("input_features shape:", input_features.shape)  # (348, 14)
    # 权重参数初始化
    # weights = torch.randn((14, 128), dtype=float, requires_grad=True)
    # biases = torch.randn((128), dtype=float, requires_grad=True)
    # weights2 = torch.randn((128, 1), dtype=float, requires_grad=True)
    # biases2 = torch.randn(1, dtype=float, requires_grad=True)
    #
    # learning_rate = 0.01
    # losses = []
    # for i in range(1000):
    #     # 计算隐层。mm (matrix multiplication)，即矩阵乘法
    #     hidden = x.mm(weights) + biases
    #     # 加入激活函数。非线性映射
    #     hidden = torch.relu(hidden)
    #     # 预测结果
    #     predictions = hidden.mm(weights2) + biases2
    #     # 计算损失。mean: 计算输入张量中所有元素的平均值
    #     loss = torch.mean((predictions - y) ** 2)  # 预测值减去实际值的平方
    #     losses.append(loss.data.numpy())
    #
    #     if i % 100 == 0:
    #         print("loss:", loss)
    #
    #     # 更新参数
    #     weights.data.add_(- learning_rate * weights.grad.data)
    #     biases.data.add_(- learning_rate * biases.grad.data)
    #     weights2.data.add_(- learning_rate * weights2.grad.data)
    #     biases2.data.add_(- learning_rate * biases2.grad.data)
    #
    #     # 每次迭代记得都清空
    #     weights.grad.data.zero_()
    #     biases.grad.data.zero_()
    #     weights2.grad.data.zero_()
    #     biases2.grad.data.zero_()

    # 更简单的构建网络模型
    input_size = input_features.shape[1]
    hidden_size = 128
    output_size = 1
    batch_size = 16
    # Sequential 连续的
    # torch.nn.Sequential 是一个容器，可以将多个层组合成一个模型
    my_nn = torch.nn.Sequential(
        torch.nn.Linear(input_size, hidden_size),
        torch.nn.Sigmoid(),  # 激活函数
        torch.nn.Linear(hidden_size, output_size)
    )
    cost = torch.nn.MSELoss(reduction="mean")
    optimizer = torch.optim.Adam(my_nn.parameters(), lr=0.01)

    # 训练网络
    losses = []
    for i in range(1000):
        batch_loss = []
        # MINI-Batch方法来进行训练
        for start in range(0, len(input_features), batch_size):
            end = start + batch_size if start + batch_size < len(input_features) else len(input_features)
            xx = torch.tensor(input_features[start:end], dtype=torch.float, requires_grad=True)
            yy = torch.tensor(labels[start: end], dtype=torch.float, requires_grad=True)
            prediction = my_nn(xx)
            loss = cost(prediction, yy)
            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()
            batch_loss.append(loss.data.numpy())
        # 打印损失
        if i % 100 == 0:
            losses.append(np.mean(batch_loss))
            print(i, np.mean(batch_loss))
