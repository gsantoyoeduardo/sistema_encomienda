from django.db import models
from django.core.validators import MinValueValidator


class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    tiempo_estimado_horas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Tiempo estimado en horas'
    )
    costo_base = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['origen', 'destino']
        unique_together = ['origen', 'destino']

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.tiempo_estimado_horas}h)"
