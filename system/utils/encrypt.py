# -*- coding = utf-8 -*-
# @Time : 2022/4/9 15:52
# @Author : Ethan
# @File : encrypt.py
# @Software : PyCharm

from django.conf import settings
import hashlib

def md5(data_string):
    '''md5加密'''
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8')) #创建md5对象，并对其字符串进行编码
    obj.update(data_string.encode('utf-8')) #将密码和加密字符串拼接加密
    return obj.hexdigest() #转换为16进制