from django.urls import path
from .views import alumni_list

urlpatterns = [
    path('', alumni_list, name='alumni'),
]