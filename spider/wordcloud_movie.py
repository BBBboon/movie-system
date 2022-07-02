# -*- coding = utf-8 -*-
# @Time : 2022/4/4 11:38
# @Author : Ethan
# @File : wordcloud_movie.py
# @Software : PyCharm


import jieba #分词
from matplotlib import pyplot as plt #绘图，数据可视化
import matplotlib.colors as colors  # 处理图片相关内容
from wordcloud import WordCloud #词云
from PIL import Image #图片处理
import numpy as np #矩阵运算
import sqlite3 #数据库


# 准备词云所需的词
con = sqlite3.connect('../db.sqlite3')
cur = con.cursor()

sql = 'select cname from system_movie'
data = cur.execute(sql)

text = ''
for item in data:
    text = text + item[0] + ' ' #将所有的介绍合成一整个字符串

cur.close()
con.close()

# 分词
# cut = jieba.cut(text)
# string = ' '.join(cut)
# print(string)

# 停用词
# stopwords = set()
# content = [line.strip() for line in open('stopwords.txt','r',encoding='UTF-8').readlines()]
# stopwords.update(content)

# 自定义文字颜色
colormaps = colors.ListedColormap(['#678bc2', '#0d61ec', '#0a90e3', '#be5cdc', '#9393f8'])

img = Image.open(r'..\system\static\img\cloud\camera.png') #打开遮罩图片
img_array = np.array(img) #将图片转换为数组
wc = WordCloud(
    colormap=colormaps,  # 指定颜色
    background_color='white', #图片背景颜色
    mask=img_array,
    font_path="HGY2_CNKI.TTF", #字体
    # stopwords=stopwords,
)
wc.generate_from_text(text)

# 绘制图片
fig = plt.figure(1) #表示定位（创建）第一个画板，如果没有参数默认创建一个新的画板
plt.imshow(wc) #调用imshow()函数实现热图绘制，通过色差、亮度来展示数据的差异
plt.axis('off') #是否显示坐标轴

# plt.show() #显示生成的词云图片
plt.savefig(r'..\system\static\img\movie_word.jpg', dpi=1800) #输出词云图片到文件


