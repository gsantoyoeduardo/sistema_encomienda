from django.contrib import admin
from clientes.models import Cliente
from rutas.models import Ruta
from envios.models import Empleado, Encomienda, HistorialEstado


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'tipo_documento', 'numero_documento', 'telefono', 'email')
    list_filter = ('tipo_documento',)
    search_fields = ('nombre_completo', 'numero_documento', 'email')
    ordering = ('nombre_completo',)


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'tiempo_estimado_horas', 'costo_base')
    list_filter = ('origen', 'destino')
    search_fields = ('origen', 'destino')
    ordering = ('origen', 'destino')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'sucursal', 'activo')
    list_filter = ('rol', 'activo', 'sucursal')
    search_fields = ('nombre', 'sucursal')
    ordering = ('nombre',)


@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'descripcion',
        'peso_kg',
        'estado',
        'remitente',
        'destinatario',
        'ruta',
        'fecha_envio',
        'fecha_entrega_estimada'
    )
    list_filter = ('estado', 'fecha_envio', 'ruta')
    search_fields = ('codigo', 'descripcion', 'remitente__nombre_completo', 'destinatario__nombre_completo')
    ordering = ('-fecha_envio',)
    raw_id_fields = ('remitente', 'destinatario', 'ruta')
    date_hierarchy = 'fecha_envio'


@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ('encomienda', 'estado', 'fecha_cambio', 'detalle_observacion')
    list_filter = ('estado', 'fecha_cambio')
    search_fields = ('encomienda__codigo', 'detalle_observacion')
    ordering = ('-fecha_cambio',)
    raw_id_fields = ('encomienda',)
