from django.urls import path
from envios import views

app_name = 'envios'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('', views.EncomiendaListView.as_view(), name='encomienda_list'),
    path('<int:pk>/', views.EncomiendaDetailView.as_view(), name='encomienda_detail'),
    path('crear/', views.EncomiendaCreateView.as_view(), name='encomienda_create'),
]
