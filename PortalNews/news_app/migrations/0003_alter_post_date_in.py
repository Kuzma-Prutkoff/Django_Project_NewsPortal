# Generated by Django 3.2.18 on 2023-04-14 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0002_auto_20230414_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_in',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
