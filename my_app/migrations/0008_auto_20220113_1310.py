# Generated by Django 3.1.5 on 2022-01-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_auto_20220113_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuntadult',
            name='categorie_adult',
            field=models.CharField(choices=[('Auto, moto si ambarcatiuni', 'Auto, moto si ambarcatiuni'), ('Piese auto', 'Piese auto'), ('Agro si industrie', 'Agro si industrie'), ('Imobiliare', 'Imobiliare'), ('Moda si frumusete', 'Moda si frumusete'), ('Electronice si electrocasnice', 'Electronice si electrocasnice'), ('Afaceri/Servicii', 'Afaceri/Servicii'), ('Animale de companie', 'Animale de companie'), ('Locuri de munca', 'Locuri de munca'), ('Sport, timp liber si Hobby', 'Sport, timp liber si Hobby'), ('Intreprinzatori autohtoni', 'Intreprinzatori autohtoni'), ('Matrimoniale', 'Matrimoniale')], max_length=264, null=True),
        ),
    ]
