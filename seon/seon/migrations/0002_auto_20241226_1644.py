# Generated by Django 2.2.28 on 2024-12-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tercero',
            name='regimen_sim',
            field=models.CharField(blank=True, choices=[('V', 'Verdadero'), ('F', 'Falso')], max_length=1, null=True, verbose_name='Régimen Simplificado'),
        ),
        migrations.AlterField(
            model_name='tercero',
            name='codter',
            field=models.CharField(help_text='Ingrese El Código del Tercero', max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Código del Tercero'),
        ),
        migrations.AlterField(
            model_name='tercero',
            name='ter_origen',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Comercial'), (1, 'Internet'), (2, 'Recomendación'), (3, 'Cursos'), (4, 'Publicidad')], null=True, verbose_name='Origen del cliente'),
        ),
    ]