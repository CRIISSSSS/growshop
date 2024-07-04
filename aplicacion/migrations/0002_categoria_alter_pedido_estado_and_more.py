# Generated by Django 5.0.6 on 2024-07-04 00:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('en proceso', 'En Proceso'), ('entregado', 'Entregado'), ('enviado', 'Enviado'), ('pendiente', 'Pendiente')], default='Pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='estado',
            field=models.CharField(choices=[('en proceso', 'En Proceso'), ('entregado', 'Entregado'), ('enviado', 'Enviado'), ('pendiente', 'Pendiente')], default='Pendiente', max_length=50),
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplicacion.categoria'),
        ),
    ]