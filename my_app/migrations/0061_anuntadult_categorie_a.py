# Generated by Django 3.1.5 on 2021-12-22 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0060_auto_20211222_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuntadult',
            name='categorie_a',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
