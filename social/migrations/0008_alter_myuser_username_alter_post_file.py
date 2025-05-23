# Generated by Django 5.1.7 on 2025-04-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_myuser_first_name_myuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='posts/'),
        ),
    ]
