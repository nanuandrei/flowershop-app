# Generated by Django 3.0 on 2020-06-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produse',
            name='tip',
            field=models.CharField(choices=[('trandafir', 'trandafir'), ('muscată', 'muscată'), ('lalea', 'lalea'), ('garoafă', 'garoafă'), ('crin', 'crin')], default='trandafir', max_length=9),
        ),
    ]
