# Generated by Django 4.1.4 on 2023-04-22 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0002_alter_profile_data_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile_data',
            old_name='user_id',
            new_name='user_name',
        ),
    ]