# Generated by Django 3.2.8 on 2021-10-27 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_comment_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='count',
            new_name='bidcount',
        ),
    ]
