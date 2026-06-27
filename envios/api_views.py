from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils import timezone

from envios.models import Encomienda, HistorialEstado
from envios.serializers import EncomiendaSerializer, EncomiendaDetailSerializer, HistorialEstadoSerializer
from sistema_encomiendas.choices import EstadoEncomienda


CLAVES_CACHE_ESTADISTICAS = [
    'cache_total_activas',
    'cache_total_en_ruta',
    'cache_total_con_retraso',
    'cache_total_entregadas',
    'cache_total_registradas',
    'cache_total_en_sucursal',
]


class EncomiendaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Encomienda.objects.con_relaciones_optimizadas()
    serializer_class = EncomiendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class EncomiendaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Encomienda.objects.con_relaciones_optimizadas()
    serializer_class = EncomiendaDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class EncomiendaViewSet(viewsets.ModelViewSet):
    queryset = Encomienda.objects.con_relaciones_optimizadas()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EncomiendaDetailSerializer
        return EncomiendaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        encomienda = self.get_object()
        nuevo_estado = request.data.get('estado')
        observacion = request.data.get('observacion', '')

        estados_validos = [choice[0] for choice in EstadoEncomienda.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Opciones válidas: {estados_validos}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if encomienda.estado == nuevo_estado:
            return Response(
                {'error': f'La encomienda ya se encuentra en estado "{nuevo_estado}".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        estado_anterior = encomienda.estado
        encomienda.estado = nuevo_estado
        encomienda.save()

        HistorialEstado.objects.create(
            encomienda=encomienda,
            estado=nuevo_estado,
            detalle_observacion=observacion
        )

        cache.delete_many(CLAVES_CACHE_ESTADISTICAS)

        return Response({
            'mensaje': f'Estado actualizado exitosamente.',
            'codigo': encomienda.codigo,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'fecha_cambio': timezone.now().isoformat(),
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='historial')
    def historial(self, request, pk=None):
        encomienda = self.get_object()
        historial = encomienda.historial_estados.order_by('-fecha_cambio')
        serializer = HistorialEstadoSerializer(historial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
