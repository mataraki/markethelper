# Generated by Django 3.2.8 on 2022-01-30 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markethelper', '0005_share_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('event_type', models.CharField(blank=True, max_length=10, null=True)),
                ('share_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='markethelper.share')),
            ],
        ),
    ]