# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 02:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=25)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CorreccionDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField()),
                ('fecha_hora', models.DateTimeField()),
                ('clasificacion_correcta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Clasificacion')),
            ],
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudio', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('objectUID', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=55)),
                ('estudio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Estudio')),
            ],
        ),
        migrations.CreateModel(
            name='SugerenciaDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_correcto', models.BooleanField(default=True)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('clasificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Clasificacion')),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Imagen')),
            ],
        ),
        migrations.AddField(
            model_name='imagen',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Series'),
        ),
        migrations.AddField(
            model_name='correcciondiagnostico',
            name='imagen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Imagen'),
        ),
        migrations.AddField(
            model_name='correcciondiagnostico',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
