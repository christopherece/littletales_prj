# Generated by Django 5.2.1 on 2025-06-02 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_config', '0007_remove_siteconfig_connect_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='connect_description',
            field=models.TextField(default='Find and connect with friends, family, and like-minded individuals.', help_text='Description for the connect feature'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='connect_heading',
            field=models.CharField(default='Connect', help_text='Heading for the connect feature', max_length=50),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='favicon',
            field=models.ImageField(blank=True, help_text='Upload a favicon (16x16px recommended)', null=True, upload_to='site_config/'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='learn_description',
            field=models.TextField(default='Discover new opportunities and grow your professional network.', help_text='Description for the learn feature'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='learn_heading',
            field=models.CharField(default='Learn', help_text='Heading for the learn feature', max_length=50),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='register_text',
            field=models.CharField(default='New here? Join our community today and start sharing your experiences.', help_text='Text for the register section', max_length=200),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='share_description',
            field=models.TextField(default='Share your thoughts, photos, and experiences with your network.', help_text='Description for the share feature'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='share_heading',
            field=models.CharField(default='Share', help_text='Heading for the share feature', max_length=50),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='sign_in_text',
            field=models.CharField(default='Already have an account? Sign in to access your feed, connect with friends, and more.', help_text='Text for the sign in section', max_length=200),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='welcome_subtitle',
            field=models.CharField(default='Connect with friends and share your experiences', help_text='Welcome page subtitle text', max_length=200),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='welcome_title',
            field=models.CharField(default='Welcome to LoopedIn', help_text='Main welcome page title', max_length=100),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='logo',
            field=models.ImageField(blank=True, help_text='Upload the site logo (30x30px recommended)', null=True, upload_to='site_config/'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='logo_name',
            field=models.CharField(default='LoopedIn', help_text='Name of your site', max_length=50),
        ),
    ]
