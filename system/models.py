from django.db import models

class UserID(models.Model):
    '''用户身份表'''
    title = models.TextField(verbose_name='用户身份') #verbose_name表示注解

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''用户表'''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # max_digits:总共占10位 decimal_places:小数位占两位 default:默认值为零
    # account = models.DecimalField(verbose_name='用户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)

    # to:与哪张表相连 to_field:与表中的哪一列关联 models.CASCADE:级联删除
    identity = models.ForeignKey(verbose_name='身份', to='UserID', to_field='id', on_delete=models.CASCADE, default=1)
    # models.SET_NULL:删除置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)
    # models.PROTECT:删除保护，必须将与要删除记录相关的表项都删除后才能删除
    # depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.PROTECT)

    # 在django中做的约束
    gender_choices = (
        (1, '男'),
        (0, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

class Comments(models.Model):
    '''电影评论表'''
    id = models.AutoField(verbose_name='序号', primary_key=True)
    # name = models.ForeignKey(verbose_name='电影', to='Movie', to_field='movie', on_delete=models.PROTECT)
    name = models.CharField(verbose_name='电影', max_length=128)
    viewer_name = models.CharField(verbose_name='用户名', max_length=32)
    star = models.CharField(verbose_name='评星', max_length=2)
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    comment = models.TextField(verbose_name='电影评论')


class Movie(models.Model):
    '''电影信息表'''
    id = models.BigAutoField(verbose_name='排名', primary_key=True)
    info_link = models.TextField(verbose_name='电影链接')
    pic_link = models.TextField(verbose_name='图片链接')
    cname = models.CharField(verbose_name='中文名', max_length=16)
    ename = models.CharField(verbose_name='英文名', max_length=64)
    score = models.DecimalField(verbose_name='评分', max_digits=2, decimal_places=1, default=0)
    rated = models.IntegerField(verbose_name='评价人数')
    introduction = models.TextField(verbose_name='电影简介')
    new_introduction = models.TextField(verbose_name='简介')
    info = models.TextField(verbose_name='演员与导演')
    movie = models.CharField(verbose_name='影片名', max_length=128)


class Admin(models.Model):
    '''管理员表'''
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username #输出时（外键连接调用）显示username


class Problem(models.Model):
    '''遇到的问题'''
    user = models.ForeignKey(verbose_name='用户id', to="UserInfo", on_delete=models.CASCADE)
    upload_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    problem = models.TextField(verbose_name='问题描述')
    img = models.FileField(verbose_name='问题截图', upload_to='problem/')


