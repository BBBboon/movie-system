# Generated by Django 4.0.1 on 2022-04-02 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_rename_name_comments_name_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='name_id',
            new_name='name',
        ),
    ]
