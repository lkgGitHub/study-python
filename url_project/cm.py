import pandas as pd

path = 'D:\\01Work\\04微智URL分析\\研判结果\\judgeresult_20200501.csv'
csv = pd.read_csv(path, header=None)
black_csv = csv[csv[7] == 100]
black_list = black_csv[0].values.tolist()
with open('black.txt', mode='w') as f:
    url_list = [url + "\n" for url in black_list]
    f.writelines(url_list)

white_csv = csv[csv[7] == 0]
white_list = white_csv[0].values.tolist()
with open('white.txt', mode='w') as f:
    url_list = [url + "\n" for url in black_list]
    f.writelines(url_list)


