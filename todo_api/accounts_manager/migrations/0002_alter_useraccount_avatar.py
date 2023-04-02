# Generated by Django 4.1.6 on 2023-03-02 12:26

import accounts_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='avatar',
            field=models.ImageField(blank=True, default='/avatar/avatar.jpg', max_length=255, null=True, upload_to=accounts_manager.models.UserAccount.avatar_path),
        ),
    ]