# Generated by Django 3.1.5 on 2022-01-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_auto_20220111_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuntadult',
            name='an_de_constructie',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='capacitate_motor',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='combustibil',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='compartimentare',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='culoare',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='cutie_de_viteze',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='etaj',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='marca',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='marime',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='mobilitatea_postului',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='nivelul_de_experienta',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='nivelul_de_studii',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='numar_de_camere',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='program_flexibil',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='rulaj',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='stare',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='suprafata_utila',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='teren',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='tip_contract',
            field=models.CharField(max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='anuntadult',
            name='tip_job',
            field=models.CharField(max_length=264, null=True),
        ),
    ]