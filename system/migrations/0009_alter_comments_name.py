# Generated by Django 4.0.1 on 2022-04-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_rename_name_id_comments_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='name',
            field=models.CharField(max_length=128, verbose_name='电影'),
        ),
    ]
