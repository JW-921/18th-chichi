# Generated by Django 5.1.4 on 2025-01-05 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_create_at_profile_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '男'), ('F', '女'), ('O', '其他')], default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
