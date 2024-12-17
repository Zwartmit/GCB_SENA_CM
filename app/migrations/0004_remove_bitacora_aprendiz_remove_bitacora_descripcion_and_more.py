# Generated by Django 5.1.4 on 2024-12-17 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_bitacora'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bitacora',
            name='aprendiz',
        ),
        migrations.RemoveField(
            model_name='bitacora',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='bitacora',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='bitacora',
            name='instructor',
        ),
        migrations.AddField(
            model_name='bitacora',
            name='actividad',
            field=models.CharField(max_length=200, null=True, verbose_name='Actividad'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='imagen',
            field=models.ImageField(null=True, upload_to='', verbose_name='Imagen'),
        ),
        migrations.CreateModel(
            name='DetalleBitacora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True, verbose_name='Fecha')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripción')),
                ('aprendiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Aprendiz', to='app.aprendiz')),
                ('bitacora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bitacora', to='app.bitacora')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Instructor', to='app.instructor')),
            ],
        ),
    ]
