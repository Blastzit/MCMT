from django.urls import path
from .views import alumni_list, alumni_detail

urlpatterns = [
    path('', alumni_list, name='alumni'),
    path('<int:id>/', alumni_detail, name='alumni_detail'),
]