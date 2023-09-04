# coding: utf-8
import pandas as pd
import numpy as np


# 读取数据
df = pd.read_csv(r"data\fyx_chinamoney.csv", header=None)

# 拿到所有数据
data = df.values

# 计算数据总长度
data_length = len(data)

# 由于是按照80分割，所以计算最大能够等分的长度
max_divisible_length = data_length // 80 * 80

# 截取最大能够等分的部分
data_sliced = data[:max_divisible_length]

# 截取剩余的部分
data_last = data[max_divisible_length:]
data_last = np.split(data_last, len(data_last) // 20)

# 将数据分割成长度为80的子数组
data_split = np.split(data_sliced, data_length // 80)

# 将剩余的部分插入到总数据中
data_split.extend(data_last)

# 打印输出
for dt in data_split:
    print(f"数据: {dt},总长度:{len(dt)}")



