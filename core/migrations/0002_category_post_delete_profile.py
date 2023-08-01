# Generated by Django 4.2.3 on 2023-08-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Категория')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], verbose_name='Рейтинг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('fhoto', models.ImageField(blank=True, null=True, upload_to='photo_post/', verbose_name='Фотография')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Unpublished', 'Unpublished')], max_length=200, verbose_name='Статус публикации')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
