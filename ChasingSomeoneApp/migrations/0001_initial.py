# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('birthday', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QrStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField()),
                ('url_profile_img', models.CharField(max_length=200)),
                ('action_type', models.CharField(max_length=50)),
                ('target', models.CharField(max_length=200)),
                ('url_target', models.CharField(max_length=200)),
                ('user_profile_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TwStatus',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('text', models.CharField(max_length=500)),
                ('img_url', models.ImageField(upload_to=b'', blank=True)),
                ('lang', models.CharField(default=b'en', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QrAccount',
            fields=[
                ('user_name', models.CharField(max_length=45)),
                ('profile_img', models.CharField(max_length=200, null=True, blank=True)),
                ('follower', models.OneToOneField(primary_key=True, serialize=False, to='ChasingSomeoneApp.Follower')),
            ],
        ),
        migrations.CreateModel(
            name='TwAccount',
            fields=[
                ('act_id', models.CharField(max_length=45)),
                ('screen_name', models.CharField(max_length=45)),
                ('both_id', models.CharField(help_text=b' Specifies the ID or screen name of the user', max_length=45, blank=True)),
                ('profile_img', models.ImageField(upload_to=b'', blank=True)),
                ('follower', models.OneToOneField(primary_key=True, serialize=False, to='ChasingSomeoneApp.Follower')),
            ],
        ),
        migrations.AddField(
            model_name='follower',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='twstatus',
            name='twAccount',
            field=models.ForeignKey(to='ChasingSomeoneApp.TwAccount'),
        ),
        migrations.AddField(
            model_name='qrstatus',
            name='qrAccount',
            field=models.ForeignKey(to='ChasingSomeoneApp.QrAccount'),
        ),
    ]
