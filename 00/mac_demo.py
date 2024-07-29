import torch

# mac
if __name__ == '__main__':
    print(torch.backends.mps.is_available())
    print(torch.backends.mps.is_built())
    device = torch.device("mps")
    print("device", device)
