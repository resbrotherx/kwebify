# Generated by Django 4.1.3 on 2023-01-04 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userinfo_bvn'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='creation_mode',
            field=models.CharField(choices=[('developer', 'developer'), ('enterprice', 'enterprice')], default='developer', max_length=400),
        ),
    ]
