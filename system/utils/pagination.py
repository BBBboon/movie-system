# -*- coding = utf-8 -*-
# @Time : 2022/4/7 16:45
# @Author : Ethan
# @File : pagination.py
# @Software : PyCharm

from django.utils.safestring import mark_safe
import copy
'''
自定义分页组件：
    若想使用分页组件，你需要这样做。
在视图函数中：
    def pretty_list(request):
        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()
        # 2.实例化分页对象
        page_object = Pagination(request, queryset)
        context = {
            'queryset': page_object.page_queryset, #分完页的数据
            'page_string': page_object.html() #页码
        }
        return render(request, 'pretty_list.html', context)
在html页面中：
        {% for obj in queryset %}
            {{ obj.xx }}
        {% endfor %}
        
        <ul class="pagination">
            {{ page_string }}
        </ul>    
'''
class Pagination(object):
    def __init__(self, request, queryset, page_param='page', page_size=9, plus=5):
        '''
            request: 请求的对象
            queryset: 符合条件的数据（根据这个条件进行分页处理）
            page_param: url中获取的分页参数，如：/pretty/list/?page=2
            page_size: 每页显示多少数据
            plus: 显示当前页的前几页或后几页
        '''

        query_dict = copy.deepcopy(request.GET) #将GET获取到的对象进行深拷贝，不然没办法直接修改GET中的内容
        query_dict._mutable = True #修改参数使query_dict的值可以修改
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()  #总条数 count():显示条数
        total_page_count, div = divmod(total_count, self.page_size)  # divmod():将两数相除，返回数组(得数，余数)
        if div:
            total_page_count += 1  # 总页码
        self.total_page_count = total_page_count

        self.plus = plus
        self.page_param = page_param

    def html(self):
        # 计算出当前页的前5页和后5页
        if self.total_page_count <= 2 * self.plus:
            # 总页数较少时
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                # 翻页到极小值
                start_page = 1
                end_page = 2 * self.plus
            else:
                if (self.page + self.plus) > self.total_page_count:
                    # 翻页到极大值
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    # 翻页到中间值
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_param, [1])  # 将page_param参数加入到query_dict中
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 设置上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)  # 将i添加到占位符中去
            page_str_list.append(ele)
        # 设置下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        # 跳转页框

        # join()方法获取可迭代对象中的所有项目，并将它们连接为一个字符串。  mark_safe()标记安全给html使其运行
        page_string = mark_safe(''.join(page_str_list))

        return page_string