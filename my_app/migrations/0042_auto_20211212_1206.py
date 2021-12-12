# Generated by Django 3.1.5 on 2021-12-12 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0041_auto_20211212_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afacere',
            name='imagine',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='anuntadult',
            name='categorie_adult',
            field=models.CharField(choices=[('Auto, moto si ambarcatiuni', 'Auto, moto si ambarcatiuni'), ('Piese auto', 'Piese auto'), ('Agro si industrie', 'Agro si industrie'), ('Imobiliare', 'Imobiliare'), ('Moda si frumusete', 'Moda si frumusete'), ('Electronice si electrocasnice', 'Electronice si electrocasnice'), ('Afaceri/Servicii', 'Afaceri/Servicii'), ('Animale de companie', 'Animale de companie'), ('Locuri de munca', 'Locuri de munca'), ('Sport, timp liber si Hobby', 'Sport, timp liber si Hobby'), ('Intreprinzatori autohtoni', 'Intreprinzatori autohtoni'), ('Matrimoniale', 'Matrimoniale')], max_length=264),
        ),
        migrations.AlterField(
            model_name='serviciu',
            name='tipul_serviciului',
            field=models.CharField(choices=[('Contabilitate', 'Contabilitate'), ('Consultanta', 'Consultanta'), ('Digital Marketing', 'Digital Marketing'), ('Grafic si Design', 'Grafic si Design'), ('Programare si tehnologie', 'Programare si tehnologie'), ('Video si animatii', 'Video si animatii')], max_length=264),
        ),
    ]
