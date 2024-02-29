# -*- coding = utf-8 -*-
# @Time : 2022/4/10 16:35
# @Author : Ethan
# @File : auth.py
# @Software : PyCharm

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, render
from system.views import UserLoginForm, LoginForm

'''
示例：

class M1(MiddlewareMixin):
    # 中间件1
    def process_request(self, request):
        # 若方法中没有返回值，就继续向后走（下个中间件）；若有返回值（HttpResponse、render、redirect），就直接返回不再向后走。
        print("M1, process_request")

    def process_response(self, request, response):
        print("M1, process_response")
        return response


class M2(MiddlewareMixin):
    # 中间件2
    def process_request(self, request):
        print("M2, process_request")

    def process_response(self, request, response):
        print("M2, process_response")
        return response
'''

management = [
    "/admin/list/", "/admin/add/", "/admin/<int:nid>/edit/", "/admin/<int:nid>/delete/",
    "/admin/<int:nid>/reset/", "/user/list/", "/user/add/", "/user/<int:nid>/edit/",
    "/user/<int:nid>/delete/", "/userid/list/", "/userid/add/", "/userid/delete/", "/userid/<int:nid>/edit/"
]

class UserMiddleware(MiddlewareMixin):
    '''检查用户登录中间件'''
    def process_request(self, request):
        if request.path_info in ["/user/login/", "/image/code/", "/home/", "/login/", "/user/logout/", "/logout/", "/user/modelform_add/"]:
            return
        if request.path_info in management:
            info_dict = request.session.get("info")
            if info_dict:
                return
            form = LoginForm()
            return render(request, "login.html", {'wrong': 1, 'form': form})
        user_info_dict = request.session.get("user_info")
        info_dict = request.session.get("info")
        if info_dict or user_info_dict:
            return
        return redirect("/user/login/")


class AuthMiddleware(MiddlewareMixin):
    '''检查管理员登录中间件'''
    def process_request(self, request):
        # 排除不需要登录就能访问的页面
        # if request.path_info in ["/login/", "/image/code/"]: #request.path_info获取当前用户请求的url
        #     return
        if request.path_info not in management:
            return
        # 读取当前用户访问的session信息。若成功读取，说明已登录过，可以继续向后。
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 若没有登陆过，则重新登录
        return redirect('/login/')