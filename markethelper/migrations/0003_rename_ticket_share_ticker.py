# Generated by Django 3.2.8 on 2021-11-29 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markethelper', '0002_alter_share_pricecurrent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='ticket',
            new_name='ticker',
        ),
    ]
