# Generated by Django 5.1.4 on 2025-01-12 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_rename_create_at_collectproject_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='cover_img/'),
        ),
    ]
