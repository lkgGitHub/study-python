# -*- coding: utf-8 -*-
import csv
import os
import numpy as np

import config
# from . import config


def load_data(data_file, usecols):
    """
       读取数据文件，加载数据
       参数：
           - data_file:    文件路径
           - usecols:      所使用的列
       返回：
           - data_arr:     数据的多维数组表示
    """
    data = []
    with open(data_file, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            row_data = []
            for col in usecols:
                str_val = row[col]
                row_data.append(float(str_val) if str_val != 'NA' else np.nan)
            # 如果行数据中不包含nan才保存该行记录
            if not any(np.isnan(row_data)):
                data.append(row_data)
    return np.array(data)

def get_polluted_perc(data_arr):
    """
         获取污染占比的小时数
         规则：
             重度污染(heavy)     PM2.5 > 150
             重度污染(medium)    75 < PM2.5 <= 150
             轻度污染(light)     35 < PM2.5 <= 75
             优良空气(good)      PM2.5 <= 35
         参数：
             - data_arr: 数据的多维数组表示
         返回：
             - polluted_perc_list: 污染小时数百分比列表
     """


def main():
    polluted_state_list = []
    for city_name, (filename, cols) in config.data_config_dict.items():
        # === Step 1+2. 数据获取 + 数据处理 ===
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + ['PM_' + col for col in cols]
        data_arr = load_data(data_file, usecols)

        print('{}共有{}行有效数据'.format(city_name, data_arr.shape[0]))
        # 预览前10行数据
        print('{}的前10行数据：'.format(city_name))
        print(data_arr[:10])

        # === Step 3. 数据分析 ===
        # 五城市污染状态，统计污染小时数的占比
        polluted_perc_list = get_polluted_perc(data_arr)
        polluted_state_list.append([city_name] + polluted_perc_list)
        print('{}的污染小时数百分比{}'.format(city_name, polluted_perc_list))

if __name__ == '__main__':
    main()
