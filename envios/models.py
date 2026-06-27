from django.db import models


class Encomienda(models.Model):
    ESTADO_CHOICES = [
        ('Registrado', 'Registrado'),
        ('En Ruta', 'En Ruta'),
        ('Entregado', 'Entregado'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Registrado')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
