# Generated by Django 5.0.6 on 2024-07-04 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0004_alter_pedido_estado_alter_seguimiento_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('enviado', 'Enviado'), ('en proceso', 'En Proceso'), ('entregado', 'Entregado'), ('pendiente', 'Pendiente')], default='Pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='estado',
            field=models.CharField(choices=[('enviado', 'Enviado'), ('en proceso', 'En Proceso'), ('entregado', 'Entregado'), ('pendiente', 'Pendiente')], default='Pendiente', max_length=50),
        ),
    ]