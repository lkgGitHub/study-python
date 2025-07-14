from torch.utils.data import Dataset


class ListDataset(Dataset):
    def __init__(self, list_path, base_path, img_size=416, augment=True, multiscale=True, normalized_labels=True):
        """ 初始化 ListDataset
        :param list_path:
        :param augment: 数据增强
        :param multiscale: 多尺度的
        :param normalized_labels: 标准化的 labels
        """
        with open(list_path, "r") as file:
            self.img_files = file.readlines()

        self.label_files = [
            path.replace("images", "labels").replace(".png", ".txt").replace(".jpg", ".txt")
            for path in self.img_files
        ]
        self.img_size = img_size
        self.max_objects = 100
        self.augment = augment
        self.multiscale = multiscale
        self.normalized_labels = normalized_labels
        self.min_size = self.img_size - 3 * 32
        self.max_size = self.img_size + 3 * 32
        self.batch_count = 0
        self.base_path = base_path

    def __getitem__(self, index):
        pass

    def __len__(self):
        return len(self.img_files)

    def collate_fn(self, batch):
        pass
