# Generated by Django 4.2 on 2025-04-04 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import social.manages


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='WEBP', keep_meta=True, null=True, quality=90, scale=None, size=[500, 500], upload_to='avatars/', verbose_name='аватарка')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('change_percentage', models.FloatField(default=0, verbose_name='Изменение')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
            managers=[
                ('objects', social.manages.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('file', models.FileField(upload_to='posts/')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание поста')),
                ('likes', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='лайки')),
                ('saved', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='сохраненные')),
                ('tag', models.CharField(max_length=900)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
        migrations.CreateModel(
            name='Saved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SavedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.post')),
                ('saved', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saved_items', to='social.saved')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='saved',
            name='post',
            field=models.ManyToManyField(related_name='saved_posts', through='social.SavedItem', to='social.post'),
        ),
        migrations.AddField(
            model_name='saved',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MyUserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('image', models.ImageField(upload_to='artist_images/', verbose_name='Фото')),
                ('artist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist_image', to=settings.AUTH_USER_MODEL, verbose_name='Фото пользователя')),
            ],
            options={
                'verbose_name': 'Аватар',
                'verbose_name_plural': 'Аватары',
            },
        ),
        migrations.CreateModel(
            name='LikeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='like_items', to='social.like')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ManyToManyField(through='social.LikeItem', to='social.post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='')),
                ('content', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='social.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
