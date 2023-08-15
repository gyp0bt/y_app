# Generated by Django 4.2.1 on 2023-08-15 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='yuser',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='yuser',
            name='pic',
            field=models.ImageField(blank=True, upload_to='profile_pics/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
