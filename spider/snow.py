# -*- coding = utf-8 -*-
# @Time : 2022/5/6 16:53
# @Author : Ethan
# @File : snow.py
# @Software : PyCharm
from snownlp import SnowNLP

text = '我今天一般般'
s = SnowNLP(text)
for sentence in s.sentences:
    print(sentence)
s1 = SnowNLP(s.sentences[0])
print(s1)
print(s1.sentiments)

