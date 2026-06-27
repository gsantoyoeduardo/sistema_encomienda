from django.db import models
from sistema_encomiendas.choices import TipoDocumento
from envios.validators import validar_documento_dni, validar_documento_ruc, validar_telefono_peru


class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=150)
    tipo_documento = models.CharField(
        max_length=3,
        choices=TipoDocumento.choices,
        default=TipoDocumento.DNI
    )
    numero_documento = models.CharField(
        max_length=11,
        unique=True,
        help_text='8 dígitos para DNI, 11 dígitos para RUC'
    )
    telefono = models.CharField(
        max_length=15,
        validators=[validar_telefono_peru],
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.nombre_completo} ({self.tipo_documento}: {self.numero_documento})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tipo_documento == TipoDocumento.DNI:
            validar_documento_dni(self.numero_documento)
        elif self.tipo_documento == TipoDocumento.RUC:
            validar_documento_ruc(self.numero_documento)
