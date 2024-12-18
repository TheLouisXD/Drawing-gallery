# Generated by Django 5.1.4 on 2024-12-11 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='descripcion',
            field=models.TextField(default='sin descripción', max_length=256, verbose_name='Descripción detallada'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='lista_dibujos',
            field=models.ManyToManyField(blank=True, related_name='categorias', to='drawing.dibujo', verbose_name='Lista de dibujos en la categoria'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='motivo',
            field=models.TextField(choices=[('contenido_inapropiado', 'Contenido inapropiado'), ('spam', 'Spam'), ('violencia', 'Contenido violento'), ('derechos_autor', 'Violación de derechos de autor'), ('otro', 'Otro')], max_length=256, verbose_name='Motivo del reporte'),
        ),
    ]
