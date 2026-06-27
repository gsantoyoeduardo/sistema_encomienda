from django.db import models
from django.utils import timezone
from datetime import timedelta


class EncomiendaQuerySet(models.QuerySet):
    def activas(self):
        return self.exclude(estado__in=['Entregado', 'Devuelto'])

    def con_retraso(self):
        fecha_actual = timezone.now()
        return self.filter(
            fecha_entrega_estimada__lt=fecha_actual
        ).exclude(estado__in=['Entregado', 'Devuelto'])

    def con_relaciones_optimizadas(self):
        return self.select_related(
            'remitente',
            'destinatario',
            'ruta'
        )

    def por_estado(self, estado):
        return self.filter(estado=estado)

    def entregadas_hoy(self):
        hoy = timezone.now().date()
        return self.filter(
            estado='Entregado',
            fecha_envio__date=hoy
        )

    def en_ruta(self):
        return self.filter(estado='En Ruta')


class EncomiendaManager(models.Manager):
    def get_queryset(self):
        return EncomiendaQuerySet(self.model, using=self._db)

    def activas(self):
        return self.get_queryset().activas()

    def con_retraso(self):
        return self.get_queryset().con_retraso()

    def con_relaciones_optimizadas(self):
        return self.get_queryset().con_relaciones_optimizadas()

    def por_estado(self, estado):
        return self.get_queryset().por_estado(estado)

    def entregadas_hoy(self):
        return self.get_queryset().entregadas_hoy()

    def en_ruta(self):
        return self.get_queryset().en_ruta()
