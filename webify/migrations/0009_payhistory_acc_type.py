# Generated by Django 4.1.3 on 2022-12-16 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webify', '0008_payhistory_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='payhistory',
            name='acc_type',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
    ]