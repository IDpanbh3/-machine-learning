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


##数据格式转换
def conversion_format():
    #xlsx转成csv
    data_xls = pd.read_excel(r'D:\实验数据\原始数据\一.数据源1.xlsx', index_col=0)
    data_xls.to_csv(r'D:\实验数据\转换数据\数据源1.csv', encoding='utf-8')

    # txt转成csv
    csvFile = open(r"D:\实验数据\转换数据\数据源2.csv",'w+',newline='',encoding='utf-8')
    writer = csv.writer(csvFile,dialect='excel')
    f = open(r"D:\实验数据\原始数据\一.数据源2-逗号间隔.txt",'r',encoding='GB2312')
    data=f.read()
    data=data.split()
    for line in data:
        line=line.split(',')
        writer.writerow(line)
    f.close()
    csvFile.close()

##合并数据
def Merge(csv_list, output_csv_path):
    for inputfile in csv_list:
        f = open(inputfile)
        data = pd.read_csv(f)
        data.to_csv(output_csv_path,encoding='gbk', mode='a', index=False)
    print('合并成功')

if __name__ == '__main__':
    conversion_format()  # 调用函数
    csv_list = glob.glob(r'D:\实验数据\转换数据\*.csv')  # 读取所有csv文件，把同文件夹下的csv文件放在csv_list
    output_csv_path = r'D:\实验数据\合并数据\合并第一版.csv'  # 将合并结果存入该路径
    print(csv_list)  # 输出找到的csv文件路径
    Merge(csv_list, output_csv_path)  # 将所有csv文件合并

# 初步去重（去表头）
df = pd.read_csv(r'D:\实验数据\合并数据\合并第一版.csv', encoding='gbk', header=None)
df.drop_duplicates(inplace=True)

#保存成新文件
list=df.values.tolist()
file=open(r'D:\实验数据\合并数据\合并第二版.csv','w+',encoding='gbk',newline='')
writer=csv.writer(file)
for i in list:
    writer.writerow(i)
file.close()

#读取新文件
df=pd.read_csv(r'D:\实验数据\合并数据\合并第二版.csv',encoding='gbk',header=0)

# 规范化
df.loc[df['ID']<202000, 'ID'] =df['ID']+202000
df.loc[df['Gender']=='boy', 'Gender'] = 'male'
df.loc[df['Gender']=='girl', 'Gender'] = 'female'
df.loc[df['Height']<3, 'Height']=df['Height']*100

# 规范化后再次去重（重复行）
df.drop_duplicates(inplace=True)
df = df.reset_index(drop=True)

##填充缺失值
def fill_vacancy1(name,df):#同一学生缺失值填充
    name_list=df[df[name].isnull()].index.tolist()
    for i in range(len(name_list)):
        for j in range(len(df)):
            if df.Name[j] == df.Name[name_list[i]] and j != name_list:
                df.loc[df.index[name_list[i]],name] = df.loc[df.index[j], name]
def fill_vacancy2(df):
    #其余缺失值填充
    df.loc[df.C3.isnull(), 'C3'] = 80
    df.loc[df.C4.isnull(), 'C4'] = int(df.C4.mean() + 0.5)
    df.loc[df.C5.isnull(), 'C5'] = int(df.C5.mean() + 0.5)
    df.loc[df.Constitution.isnull(), 'Constitution'] = "general"

fill_vacancy1('Height',df)
fill_vacancy1('C1',df)
fill_vacancy1('C2',df)
fill_vacancy1('C3',df)
fill_vacancy1('C4',df)
fill_vacancy1('C5',df)
fill_vacancy1('C6',df)
fill_vacancy1('C7',df)
fill_vacancy1('C8',df)
fill_vacancy1('C9',df)
fill_vacancy1('Constitution',df)
fill_vacancy2(df)

# 按ID号排序
df.sort_values(by='ID', inplace=True, ascending=True)
# 重置行索引
df = df.reset_index(drop=True)

# 数据中存在ID相同，其他特征值不同的情况，同ID去重
drop_list = []  # 用于存放记录重复行序列
for i in df.index:
    for j in df.index:
        if df.ID[j] == df.ID[i] and j > i:
            drop_list.append(j)
drop_dup_list = sorted(set(drop_list))  # 列表去重并排序
for line in drop_dup_list:
    df.drop([line], inplace=True)

# 去重后重置行索引
df = df.reset_index(drop=True)
print(df)
print('数据清洗成功!')

# 保存最终文件
df.to_csv(r'D:\实验数据\合并数据\合并数据最终版.csv', encoding='gbk', mode='a',index=False)