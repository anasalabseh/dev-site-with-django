# Generated by Django 3.2.8 on 2022-08-12 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='images\\default.jpg', null=True, upload_to=''),
        ),
    ]
