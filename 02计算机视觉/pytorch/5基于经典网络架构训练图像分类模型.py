import os.path

from mpmath.identification import transforms
import torch.optim as optim
import torchvision
from torchvision import transforms, models, datasets

if __name__ == '__main__':
    data_dir = './flower_data/'
    train_dir = data_dir + '/train'
    valid_dir = data_dir + '/valid'

    data_transform = {
        'train':
            transforms.Compose([
                transforms.Resize([96, 96]),

                transforms.RandomRotation(45),  # 随机旋转，-45到45度之间随机选
                transforms.CenterCrop(64),  # 从中心开始裁剪
                transforms.RandomHorizontalFlip(p=0.5),  # 随机水平翻转 选择一个概率概率
                transforms.RandomVerticalFlip(p=0.5),  # 随机垂直翻转
                # 参数1为亮度，参数2为对比度，参数3为饱和度，参数4为色相
                transforms.ColorJitter(brightness=0.2, contrast=0.1, saturation=0.1, hue=0.1),
                transforms.RandomGrayscale(p=0.025),  # 概率转换成灰度率，3通道就是R=G=B

                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 均值，标准差
            ]),
        'valid':
            transforms.Compose([
                transforms.Resize([64, 64]),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
    }

    base_size = 128
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transform[x]) for x in ['train', 'valid']}
