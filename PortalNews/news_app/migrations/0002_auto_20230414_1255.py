# Generated by Django 3.2.18 on 2023-04-14 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'Категория новости', 'verbose_name_plural': 'Категории новостей'},
        ),
        migrations.AlterField(
            model_name='post',
            name='date_in',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
