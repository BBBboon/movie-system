# Generated by Django 4.0.1 on 2022-03-31 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='排名')),
                ('info_link', models.TextField(verbose_name='电影链接')),
                ('pic_link', models.TextField(verbose_name='图片链接')),
                ('cname', models.CharField(max_length=16, verbose_name='中文名')),
                ('ename', models.CharField(max_length=64, verbose_name='英文名')),
                ('score', models.DecimalField(decimal_places=1, default=0, max_digits=2, verbose_name='评分')),
                ('rated', models.IntegerField(verbose_name='评价人数')),
                ('introduction', models.TextField(verbose_name='电影简介')),
                ('info', models.TextField(verbose_name='演员与导演')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.department', verbose_name='部门'),
        ),
    ]
