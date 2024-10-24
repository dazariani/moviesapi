# Generated by Django 5.1.1 on 2024-09-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0003_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='images/posters/'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, upload_to='images/users/'),
        ),
    ]