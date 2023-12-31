# Generated by Django 4.2.3 on 2023-08-17 09:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='link_fb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to='profile.photo/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegram',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='short',
            name='viewed_users',
            field=models.ManyToManyField(blank=True, related_name='viewed_shorts', to=settings.AUTH_USER_MODEL),
        ),
    ]
