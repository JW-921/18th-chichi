# Generated by Django 5.1.4 on 2024-12-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0003_faq_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['position']},
        ),
        migrations.RenameField(
            model_name='faq',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='update_at',
        ),
        migrations.AddField(
            model_name='faq',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='faq',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
