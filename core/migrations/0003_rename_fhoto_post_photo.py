# Generated by Django 4.2.3 on 2023-08-01 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_post_delete_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='fhoto',
            new_name='photo',
        ),
    ]
