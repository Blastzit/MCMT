from django.shortcuts import render
from .models import Alumni

def alumni_list(request):
    alumni_list = Alumni.objects.all()
    return render(request, 'alumni/alumni.html', {'alumni_list': alumni_list})

def alumni_detail(request, id):
    alumni = Alumni.objects.get(id=id)
    return render(request, 'alumni/alumni_detail.html', {'alumni': alumni})