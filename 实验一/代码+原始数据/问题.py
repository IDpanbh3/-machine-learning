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


#读取数据
df=pd.read_csv(r'D:\实验数据\合并数据\合并数据最终版.csv',encoding='gbk',header=0)
def avg_Beijing(CX):
#计算北京学生的平均成绩
#CX代表传入的课程名
    CX_list=df.loc[df["City"]=="Beijing",CX].tolist() #用CX_list列表存放传入数据
    sum=0 #sum计算课程中所有数字总和
    for i in CX_list:
        sum=sum+i;
    avg=sum/len(CX_list)  #avg用来存平均成绩
    print(CX+'平均成绩：'+str(avg))
print('问题1：')
avg_Beijing('C1')
avg_Beijing('C2')
avg_Beijing('C3')
avg_Beijing('C4')
avg_Beijing('C5')
avg_Beijing('C6')
avg_Beijing('C7')
avg_Beijing('C8')
avg_Beijing('C9')

print('问题2：')
cond1=df.loc[df.City=='Guangzhou']
cond2=cond1.loc[cond1.Gender=='male']
cond3=cond2.loc[cond2.C1>80]
cond4=cond3.loc[cond3.C9>9]
print('数量： ',len(cond4))

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

print('问题3：')
#计算广州女生的平均体能成绩
gz1=df.loc[df.City=='Guangzhou']
gz2=gz1.loc[gz1.Gender=='female']
gz_cons=gz2.Constitution
gz_cons=list(gz_cons)
rand(gz_cons) #体能成绩量化
gz_avg=round(np.mean(gz_cons),1) #计算平均值并保存一位小数
print('广州女生平均体能成绩为： ',gz_avg)
#计算上海女生的平均体能成绩
sh1=df.loc[df.City=='Shanghai']
sh2=sh1.loc[sh1.Gender=='female']
sh_cons=sh2.Constitution
sh_cons=list(sh_cons)
rand(sh_cons)
sh_avg=round(np.mean(sh_cons),1)
print('上海女孩平均体能成绩为： ',sh_avg)
#比较体能成绩
if gz_avg>sh_avg:
    print('广州女孩体能更强.')
else:
    print('上海女孩体能更好强.')


print('问题4：',)
cons_list=list(df.Constitution)
rand(cons_list) #体能成绩量化
r_df=df[['C1','C2','C3','C4','C5','C6','C7','C8','C9']].values #提取前九门成绩
array_df=np.c_[r_df,cons_list] #体能成绩和其他成绩拼接矩阵
m=array_df.shape[0] #获取矩阵行数
n=array_df.shape[1] #获取矩阵列数
array_z = np.zeros((m, n), dtype=np.float) #创建一个空矩阵
for i in range(array_df.shape[1]):
    avg=sum(array_df[:, i]) / len(array_df[:, i]) #列平均值
    variance = sum([(x - avg) ** 2 for x in array_df[:, i]]) / len(array_df[:, i]) #列方差
    stan = math.sqrt(variance) #列标准差
    for j in range(array_df.shape[0]):
        array_z[j,i]=(array_df[j,i]-avg)/stan
cor=[] #创建空列表存放相关系数
for i in range(array_z.shape[1]-1):
    sum=0
    for j in range(array_z.shape[0]):
        sum+=array_z[j,i]*array_z[j,array_z.shape[1]-1]
    cor.append(round(sum/array_z.shape[0],3))
print('相关性：',cor)