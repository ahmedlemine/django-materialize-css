# Generated by Django 4.0.6 on 2022-07-23 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='blank.jpg', upload_to='images/'),
        ),
    ]
