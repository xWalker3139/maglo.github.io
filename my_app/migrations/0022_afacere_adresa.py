# Generated by Django 3.1.5 on 2021-11-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0021_afacere_serviciu'),
    ]

    operations = [
        migrations.AddField(
            model_name='afacere',
            name='adresa',
            field=models.CharField(max_length=264, null=True),
        ),
    ]
