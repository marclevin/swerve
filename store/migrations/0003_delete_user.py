# Generated by Django 4.1 on 2022-08-26 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_user_staff'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]