# Generated by Django 4.2 on 2025-04-04 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_remove_post_image_post_file_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='saved',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='сохраненные'),
        ),
    ]
