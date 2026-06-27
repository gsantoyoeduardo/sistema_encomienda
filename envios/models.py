from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from sistema_encomiendas.choices import (
    RolEmpleado,
    EstadoEncomienda,
    TipoHistorial
)
from envios.validators import validar_peso_positivo, validar_codigo_encomienda
from envios.managers import EncomiendaManager


class Empleado(models.Model):
    nombre = models.CharField(max_length=150)
    rol = models.CharField(
        max_length=20,
        choices=RolEmpleado.choices,
        default=RolEmpleado.OPERADOR
    )
    sucursal = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()}) - {self.sucursal}"


class Encomienda(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        validators=[validar_codigo_encomienda]
    )
    descripcion = models.TextField()
    peso_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[validar_peso_positivo]
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoEncomienda.choices,
        default=EstadoEncomienda.REGISTRADO
    )
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateTimeField(
        help_text='Fecha estimada de entrega'
    )
    remitente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='encomiendas_remitente'
    )
    destinatario = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='encomiendas_destinatario'
    )
    ruta = models.ForeignKey(
        'rutas.Ruta',
        on_delete=models.PROTECT,
        related_name='encomiendas'
    )

    objects = EncomiendaManager()

    class Meta:
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion} ({self.estado})"

    def clean(self):
        if self.remitente_id and self.destinatario_id:
            if self.remitente == self.destinatario:
                raise ValidationError({
                    'destinatario': 'El destinatario no puede ser el mismo que el remitente.'
                })

        if self.fecha_entrega_estimada and self.fecha_envio:
            if self.fecha_entrega_estimada <= self.fecha_envio:
                raise ValidationError({
                    'fecha_entrega_estimada': 'La fecha de entrega estimada debe ser posterior a la fecha de envío.'
                })

    def esta_entregada(self):
        return self.estado == EstadoEncomienda.ENTREGADO

    def esta_en_ruta(self):
        return self.estado == EstadoEncomienda.EN_RUTA

    def dias_transcurridos(self):
        if self.fecha_envio:
            return (timezone.now() - self.fecha_envio).days
        return 0


class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(
        Encomienda,
        on_delete=models.CASCADE,
        related_name='historial_estados'
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoEncomienda.choices
    )
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    detalle_observacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historiales de Estado'
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.encomienda.codigo} → {self.estado} ({self.fecha_cambio.strftime('%Y-%m-%d %H:%M')})"
