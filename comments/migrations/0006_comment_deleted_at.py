# Generated by Django 5.1.4 on 2025-01-10 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_rename_create_at_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted_at',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]
