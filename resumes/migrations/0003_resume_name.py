# Generated by Django 4.0.1 on 2022-02-24 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0002_alter_resume_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='name',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
