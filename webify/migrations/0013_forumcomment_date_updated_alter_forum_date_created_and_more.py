# Generated by Django 4.1.3 on 2023-01-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webify', '0012_forumcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumcomment',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
