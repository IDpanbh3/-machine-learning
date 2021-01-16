import pandas as pd
import numpy as np
import random
import glob
import csv
import xlrd
import math
import matplotlib.pyplot as plt
import re
import seaborn

plt.rcParams['font.sans-serif'] = ['SimHei']#设置字体为SimHei显示中文
plt.rcParams['axes.unicode_minus'] = False#设置正常显示字符
np.set_printoptions(threshold=np.inf)#避免省略号问题
pd.set_option('display.width', None)# pandas设置显示宽度
pd.set_option('display.max_colwidth', 10000)#显示的最大行数和列数
pd.set_option('display.max_columns', None)# 设置显示最大列数
pd.set_option('display.max_rows', None)# 设置显示最大行数


#体能成绩量化
def rand(c_list): #随机生成某范围内的量化成绩
    for i in range(len(c_list)):
        if c_list[i] == 'bad':
            c_list[i]=random.randint(60,70)#返回60-70范围内的整数
        if c_list[i]=='general':
            c_list[i]=random.randint(70,80)
        if c_list[i]=='good':
            c_list[i]=random.randint(80,90)
        if c_list[i]=='excellent':
            c_list[i]=random.randint(90,100)


# 读取数据
df = pd.read_csv(r'D:\实验数据\合并数据\合并数据最终版.csv', encoding='gbk', header=0)

# 散点图
x=df.C1 #获取C1成绩
y=df.Constitution #获取体能成绩
x_list=list(x)#将数据放进list列表
y_list=list(y)
rand(y_list) #体能成绩量化
plt.xlabel('课程1')
plt.ylabel('体能成绩')
plt.title('散点图')
#输入X和Y作为location，size=25，颜色为blue，透明度alpha为50%
plt.scatter(x_list,y_list,c='blue',alpha=0.5,s=25)
plt.show()

# 直方图
x=df.C1
x_list=list(x)
bins=[60,65,70,75,80,85,90,95,100]
plt.hist(x_list, bins=bins, histtype='bar',edgecolor ='black',alpha=0.5)
plt.xlabel('分数')
plt.ylabel('数量')
plt.title('C1成绩直方图')
plt.show()