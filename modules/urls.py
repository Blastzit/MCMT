from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_dashboard, name='module_dashboard'),
    path('module-information/', views.module_information, name='module_information'),
    path('module-graph/', views.module_graph, name='module_graph'),
    path('<str:module_code>/', views.module_detail, name='module_detail'),
]