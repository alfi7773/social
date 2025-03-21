# Generated by Django 4.2 on 2025-03-20 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_alter_myuser_user_alter_myuserimage_artist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saved',
            field=models.PositiveIntegerField(default=0, verbose_name='сохраненные'),
        ),
        migrations.AlterField(
            model_name='saved',
            name='post',
            field=models.ManyToManyField(related_name='saved_posts', through='social.SavedItem', to='social.post'),
        ),
    ]
