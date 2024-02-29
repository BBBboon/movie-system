# Generated by Django 4.0.1 on 2022-04-12 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='用户身份')),
            ],
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='account',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='depart',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='申请时间'),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='identity',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='system.userid', verbose_name='身份'),
        ),
    ]
