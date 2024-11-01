import os, yaml
from django.conf import settings
from django.shortcuts import render
from modules.utils import *
from modules.models import Assessment, Module
from fuzzywuzzy import process
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

# View for assessments
def assessment_view(request):
    selected_year = request.GET.get('year', 'Year 1')
    selected_modules = request.GET.getlist('module', [])  

    modules_by_year = get_modules_by_year()

    modules_for_selected_year = modules_by_year.get(selected_year, [])

    assessments = Assessment.objects.filter(module_name__in=selected_modules)

    context = {
        'selected_year': selected_year,
        'selected_modules': selected_modules,
        'modules_by_year': modules_by_year,
        'modules_for_selected_year': modules_for_selected_year,
        'assessments': assessments,
    }
    return render(request, 'assessment.html', context)

def get_fuzzy_matches(query, module_list, limit=5):
    return process.extract(query, module_list, limit=limit)

def load_degree_data():
    yaml_path = os.path.join(settings.STATIC_ROOT, 'degree.yaml')
    with open(yaml_path, 'r') as file:
        degree_data = yaml.safe_load(file)
    return degree_data

def degree_view(request):
    degree_data = load_degree_data()

    degree = request.GET.get('degree', 'G100')[:4]
    year = request.GET.get('year', 'Year 2')[5]
    if (degree != 'G103' and degree != 'G104') and year == '4':
        year = '3'
    search_query = request.GET.get('search', '')

    degree_list = [f"{d} {degree_data[d]['description']}" for d in degree_data['degrees']]
    modules = get_modules_by_year()

    guideline = degree_data['default']['year'+year]['guideline']
    highlight = []
    if 'year' + year in degree_data[degree]:
        guideline += "<br />" + degree_data[degree]['year'+year]['guideline']
        highlight = degree_data[degree]['year'+year]['highlight']

    module_names = [module.name for module in modules['Year '+year]]
    fuzzy_suggestions = []

    if search_query:
        fuzzy_suggestions = get_fuzzy_matches(search_query, module_names)

    if year == "2":
        compulsory_modules = [module for module in modules['Year 2'] if '/' in module.code]
        group_a_modules = [module for module in modules['Year 2'] if module.name == "i-Explore"]
        group_b_modules = [module for module in modules['Year 2'] if module not in compulsory_modules and module not in group_a_modules]
        modules = {
            'compulsory': compulsory_modules,
            'group_a': group_a_modules,
            'group_b': group_b_modules
        }
    elif year == "4" and (degree == "G103" or degree == "G104"):
        modules = {
            'year_3': modules['Year 3'],
            'year_4': modules['Year 4']
        }
    else:
        modules = {
            'all': modules['Year '+year]
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'fuzzy_suggestions': fuzzy_suggestions,
        })

    context = {
        'degree': degree,
        'degree_list': degree_list,
        'year': year,
        'modules': modules,
        'guideline': guideline,
        'highlight': highlight,
        'fuzzy_suggestions': fuzzy_suggestions,
        'search_query': search_query
    }

    return render(request, 'degree.html', context)

#Our team
def our_team_view(request):
    return render(request, 'our_team.html')