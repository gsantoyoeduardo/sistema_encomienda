from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.urls import reverse_lazy

from envios.models import Encomienda, HistorialEstado
from envios.forms import EncomiendaForm
from sistema_encomiendas.choices import EstadoEncomienda


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        total_activas = Encomienda.objects.activas().count()
        total_en_ruta = Encomienda.objects.filter(estado=EstadoEncomienda.EN_RUTA).count()
        total_con_retraso = Encomienda.objects.con_retraso().count()
        total_entregadas = Encomienda.objects.filter(estado=EstadoEncomienda.ENTREGADO).count()
        total_registradas = Encomienda.objects.filter(estado=EstadoEncomienda.REGISTRADO).count()
        total_en_sucursal = Encomienda.objects.filter(estado=EstadoEncomienda.EN_SUCURSAL).count()

        context = {
            'total_activas': total_activas,
            'total_en_ruta': total_en_ruta,
            'total_con_retraso': total_con_retraso,
            'total_entregadas': total_entregadas,
            'total_registradas': total_registradas,
            'total_en_sucursal': total_en_sucursal,
        }
        return render(request, 'envios/dashboard.html', context)


class EncomiendaListView(LoginRequiredMixin, ListView):
    model = Encomienda
    template_name = 'envios/encomienda_list.html'
    context_object_name = 'encomiendas'
    paginate_by = 15

    def get_queryset(self):
        queryset = Encomienda.objects.con_relaciones_optimizadas()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        context['choices_estado'] = EstadoEncomienda.choices
        return context


class EncomiendaDetailView(LoginRequiredMixin, DetailView):
    model = Encomienda
    template_name = 'envios/encomienda_detail.html'
    context_object_name = 'encomienda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historial'] = self.object.historial_estados.order_by('-fecha_cambio')
        return context


class EncomiendaCreateView(LoginRequiredMixin, CreateView):
    model = Encomienda
    form_class = EncomiendaForm
    template_name = 'envios/encomienda_form.html'
    success_url = reverse_lazy('envios:encomienda_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Encomienda "{self.object.codigo}" registrada exitosamente.')
        return response
