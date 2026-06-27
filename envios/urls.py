from django.urls import path, include
from rest_framework.routers import DefaultRouter
from envios import views, api_views

app_name = 'envios'

router = DefaultRouter()
router.register(r'api/encomiendas', api_views.EncomiendaViewSet, basename='encomienda-api')

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('', views.EncomiendaListView.as_view(), name='encomienda_list'),
    path('<int:pk>/', views.EncomiendaDetailView.as_view(), name='encomienda_detail'),
    path('crear/', views.EncomiendaCreateView.as_view(), name='encomienda_create'),
    path('api/list/', api_views.EncomiendaListCreateAPIView.as_view(), name='api_encomienda_list'),
    path('api/detail/<int:pk>/', api_views.EncomiendaRetrieveUpdateDestroyAPIView.as_view(), name='api_encomienda_detail'),
    path('', include(router.urls)),
]
