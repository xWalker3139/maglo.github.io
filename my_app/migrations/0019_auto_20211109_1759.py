# Generated by Django 3.1.5 on 2021-11-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0018_auto_20211109_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='MesajAdult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesaj', models.TextField(max_length=624)),
            ],
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='subcategorie_adult',
            field=models.CharField(max_length=264, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='anuntadult',
            name='imagine',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
