# Generated by Django 5.1.1 on 2024-10-21 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0015_remove_actor_firstname_remove_actor_lastname_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='movie',
            name='url',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
