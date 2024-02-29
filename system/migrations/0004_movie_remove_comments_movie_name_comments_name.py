# Generated by Django 4.0.1 on 2022-04-02 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(verbose_name='排名')),
                ('info_link', models.TextField(verbose_name='电影链接')),
                ('pic_link', models.TextField(verbose_name='图片链接')),
                ('cname', models.CharField(max_length=16, verbose_name='中文名')),
                ('ename', models.CharField(max_length=64, verbose_name='英文名')),
                ('score', models.DecimalField(decimal_places=1, default=0, max_digits=2, verbose_name='评分')),
                ('rated', models.IntegerField(verbose_name='评价人数')),
                ('introduction', models.TextField(verbose_name='电影简介')),
                ('new_introduction', models.TextField(verbose_name='简介')),
                ('info', models.TextField(verbose_name='演员与导演')),
                ('movie', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='影片名')),
            ],
        ),
        migrations.RemoveField(
            model_name='comments',
            name='movie_name',
        ),
        migrations.AddField(
            model_name='comments',
            name='name',
            field=models.ForeignKey(default='movie', on_delete=django.db.models.deletion.PROTECT, to='system.movie', verbose_name='电影名'),
        ),
    ]
