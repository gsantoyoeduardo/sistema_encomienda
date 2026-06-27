from rest_framework import serializers
from django.utils import timezone
from envios.models import Encomienda, HistorialEstado
from clientes.models import Cliente
from rutas.models import Ruta


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_completo', 'tipo_documento', 'numero_documento', 'telefono', 'email']


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['id', 'origen', 'destino', 'tiempo_estimado_horas', 'costo_base']


class EncomiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encomienda
        fields = [
            'id',
            'codigo',
            'descripcion',
            'peso_kg',
            'estado',
            'fecha_envio',
            'fecha_entrega_estimada',
            'remitente',
            'destinatario',
            'ruta',
        ]


class EncomiendaDetailSerializer(serializers.ModelSerializer):
    remitente = ClienteSerializer(read_only=True)
    destinatario = ClienteSerializer(read_only=True)
    ruta = RutaSerializer(read_only=True)
    tiene_retraso = serializers.SerializerMethodField()
    dias_transcurridos = serializers.SerializerMethodField()

    class Meta:
        model = Encomienda
        fields = [
            'id',
            'codigo',
            'descripcion',
            'peso_kg',
            'estado',
            'fecha_envio',
            'fecha_entrega_estimada',
            'remitente',
            'destinatario',
            'ruta',
            'tiene_retraso',
            'dias_transcurridos',
        ]

    def get_tiene_retraso(self, obj):
        if obj.estado in ['Entregado', 'Devuelto']:
            return False
        if obj.fecha_entrega_estimada:
            return timezone.now() > obj.fecha_entrega_estimada
        return False

    def get_dias_transcurridos(self, obj):
        if obj.fecha_envio:
            return (timezone.now() - obj.fecha_envio).days
        return 0


class HistorialEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEstado
        fields = ['id', 'estado', 'fecha_cambio', 'detalle_observacion']
