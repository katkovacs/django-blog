# Generated by Django 4.2.7 on 2023-11-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_likes'),
        ('user_profile', '0003_userprofile_followers_userprofile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to='posts.post'),
        ),
    ]
