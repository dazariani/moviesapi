# Generated by Django 5.1.1 on 2024-10-21 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0016_alter_movie_options_movie_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='url',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
