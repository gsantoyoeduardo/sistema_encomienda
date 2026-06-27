from django.db import models


class TipoDocumento(models.TextChoices):
    DNI = 'DNI', 'DNI'
    RUC = 'RUC', 'RUC'


class RolEmpleado(models.TextChoices):
    ADMINISTRADOR = 'Administrador', 'Administrador'
    CONDUCTOR = 'Conductor', 'Conductor'
    OPERADOR = 'Operador', 'Operador'


class EstadoEncomienda(models.TextChoices):
    REGISTRADO = 'Registrado', 'Registrado'
    EN_RUTA = 'En Ruta', 'En Ruta'
    EN_SUCURSAL = 'En Sucursal', 'En Sucursal'
    ENTREGADO = 'Entregado', 'Entregado'
    DEVUELTO = 'Devuelto', 'Devuelto'


class TipoHistorial(models.TextChoices):
    CAMBIO_ESTADO = 'Cambio Estado', 'Cambio Estado'
    OBSERVACION = 'Observación', 'Observación'
