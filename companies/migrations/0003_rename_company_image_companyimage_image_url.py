# Generated by Django 4.0.1 on 2022-02-16 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_companyimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyimage',
            old_name='company_image',
            new_name='image_url',
        ),
    ]