# Generated by Django 3.0.5 on 2020-04-26 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategorie',
            },
        ),
        migrations.CreateModel(
            name='Zrodlo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Zrodlo',
                'verbose_name_plural': 'Źródło',
            },
        ),
        migrations.CreateModel(
            name='Wydatek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=60)),
                ('opis', models.TextField(blank=True)),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=99999999)),
                ('kategoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Budzet.Kategoria')),
            ],
            options={
                'verbose_name': 'Wydatek',
                'verbose_name_plural': 'Wydatki',
            },
        ),
        migrations.CreateModel(
            name='Dochod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=60)),
                ('opis', models.TextField(blank=True)),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=9999999)),
                ('zrodlo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Budzet.Zrodlo')),
            ],
            options={
                'verbose_name': 'Dochod',
                'verbose_name_plural': 'Dochody',
            },
        ),
    ]