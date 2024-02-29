# -*- coding = utf-8 -*-
# @Time : 2022/4/9 9:59
# @Author : Ethan
# @File : bootstrap.py
# @Software : PyCharm

from django import forms

class BootStrap:
    bootstrap_exclude_fields = [] #将不想添加bootstrap样式的元素加在这里

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加class='form-control'
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，在原有基础上进行添加；否则，直接添加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


# 写好父类的ModelForm，重复只用是需要继承
class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass

class BootStrapForm(BootStrap, forms.Form):
    pass