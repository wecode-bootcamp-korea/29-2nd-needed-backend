# Generated by Django 4.0.1 on 2022-02-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NeededPlus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=50)),
                ('needed_plus_image', models.CharField(max_length=50)),
                ('period', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'needed_plus',
            },
        ),
    ]
