from django.db import models
from django.forms import ValidationError
from .choices import programas

class Aprendiz(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        RC = 'RC', 'Registro Civil'
        
    nombre = models.CharField(max_length=200, null=True, blank=False, verbose_name='Nombre')
    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC, verbose_name="Tipo de documento")
    num_documento = models.PositiveIntegerField(null=True, blank=False, verbose_name='Nº de documento')
    correo = models.EmailField(null=True, blank=False, verbose_name='Correo')
    num_ficha = models.PositiveIntegerField(null=True, blank=False, verbose_name='Ficha')
    programa_formacion = models.CharField(max_length=100, choices=[(prog, prog) for prog in programas], null=True, blank=False, verbose_name='Programa de formación')
    fecha_inicio_programa = models.DateField(null=True, blank=False, verbose_name='Fecha de inicio del programa de formación')

    def __str__(self):
        return f"Aprendiz: {self.nombre}"

    class Meta:
        verbose_name = "Aprendiz"
        verbose_name_plural = "Aprendices"
        db_table = 'Aprendiz'

class Instructor(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        RC = 'RC', 'Registro Civil'
        
    nombre = models.CharField(max_length=200, null=True, blank=False, verbose_name='Nombre')
    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC, verbose_name="Tipo de documento")
    num_documento = models.PositiveIntegerField(null=True, blank=False, verbose_name='Nº de documento')
    correo = models.EmailField(null=True, blank=False, verbose_name='Correo')

    def __str__(self):
        return f"Instructor: {self.nombre}"

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"
        db_table = 'Instructor'

class Bitacora(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='Aprendiz',)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, verbose_name="Instructor")
    fecha = models.DateField(null=True, blank=False, verbose_name='Fecha')
    descripcion = models.TextField(null=True, blank=False, verbose_name='Descripción')

    def __str__(self):
        return f"Bitácoras del aprendiz: {self.aprendiz}"

    class Meta:
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácoras"
        db_table = "Bitacora"