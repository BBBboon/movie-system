# Generated by Django 4.0.1 on 2022-04-09 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_delete_movieinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
    ]