# Generated by Django 5.2.1 on 2025-06-02 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('parent', 'Parent'), ('teacher', 'Teacher'), ('admin', 'Administrator')], default='parent', max_length=10),
        ),
    ]
