# Generated by Django 4.2 on 2025-03-19 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='myuserimage',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist_image', to='social.myuser', verbose_name='Фото пользователя'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=90, scale=None, size=[1920, 1080], upload_to='posts/'),
        ),
    ]
