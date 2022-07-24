# Generated by Django 3.1.5 on 2022-07-18 17:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0010_auto_20220714_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuntcopil',
            name='favorit',
            field=models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='anuntcopil',
            name='moneda',
            field=models.CharField(blank=True, choices=[('Euro', 'Euro'), ('Lei', 'Lei')], max_length=264, null=True),
        ),
    ]
