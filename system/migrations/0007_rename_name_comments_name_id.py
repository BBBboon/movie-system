# Generated by Django 4.0.1 on 2022-04-02 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_alter_comments_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='name',
            new_name='name_id',
        ),
    ]