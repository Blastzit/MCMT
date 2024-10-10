from django.shortcuts import render
from .utils import *
from .modules_graph import G, plot, graph_renderer, highlight_modules
from .models import Assessment
from django.shortcuts import render

def filter_modules(modules, selected_terms, selected_categories):
    return [
        module for module in modules
        if any(term in (module.term if module else '') for term in selected_terms) and
           any(not module.category or category in (module.category if module else '') for category in selected_categories)
    ]

def module_dashboard(request):
    modules_by_year = get_modules_by_year()
    choose_modules_obj = []

    selected_years = request.GET.getlist('year', list(modules_by_year.keys()))
    for year in selected_years:
        if year.isdigit():
            selected_years.remove(year)
            selected_years.append("Year " + year)
    selected_terms = request.GET.getlist('term', ['Autumn', 'Spring', 'Summer'])
    selected_categories = request.GET.getlist('category', ['Pure', 'Applied', 'Statistics', 'Finance'])
    search_term = request.GET.get('search_term', '')
    choose_modules = request.GET.get('choose_modules', '')

    if isinstance(choose_modules, str):
        choose_modules = choose_modules.split(',')

    if choose_modules == ['']:
        choose_modules = []

    filtered_modules = []
    for year in selected_years:
        filtered_modules.extend(filter_modules(modules_by_year[year], selected_terms, selected_categories))

    if search_term:
        matched_modules = search_keywords(search_term)
        if matched_modules:
            filtered_modules = [module for module in filtered_modules if module.code in [m['module_code'] for m in matched_modules]]

    if choose_modules:
        module_codes = []
        for name in choose_modules:
            module = get_module_by_name(name)
            if module:
                module_codes.append(module.code)
                append_module_info(module)
                choose_modules_obj.append(module)
        highlight_modules(G, plot, graph_renderer, module_codes)
    else:
        if set(G.nodes).issubset([module.code for module in filtered_modules]):
            highlight_modules(G, plot, graph_renderer, [])
        else:
            highlight_modules(G, plot, graph_renderer, [module.code for module in filtered_modules])

    with open("modules_network.html", "r") as f:
        html_content = f.read()

    context = {
        'selected_years': selected_years,
        'selected_terms': selected_terms,
        'selected_categories': selected_categories,
        'years': list(modules_by_year.keys()),
        'terms': ['Autumn', 'Spring', 'Summer'],
        'categories': ['Pure', 'Applied', 'Statistics', 'Finance'],
        'filtered_modules': filtered_modules,
        'html_content': html_content,
        'modules': get_modules(),
        'choose_modules': choose_modules,
        'choose_modules_obj': choose_modules_obj,
        'search_term': search_term
    }

    return render(request, 'modules/module_dashboard.html', context)

def module_information(request):
    modules_by_year = get_modules_by_year()

    selected_year = request.GET.get('year', 'Year 1')
    if selected_year.isdigit():
        selected_year = "Year " + selected_year
    selected_term = request.GET.get('term', 'Autumn')

    context = {
        'selected_year': selected_year,
        'selected_term': selected_term,
        'years': list(modules_by_year.keys()),
        'filtered_modules': filter_modules(modules_by_year[selected_year], [selected_term], ['Pure', 'Applied', 'Statistics', 'Finance']),
    }

    return render(request, 'modules/module_information.html', context)

def module_graph(request):
    choose_modules = request.GET.get('choose_modules', '')
    search_term = request.GET.get('search_term', '')

    if isinstance(choose_modules, str):
        choose_modules = choose_modules.split(',')

    if choose_modules == ['']:
        choose_modules = []

    if choose_modules:
        module_codes = []
        for name in choose_modules:
            module = get_module_by_name(name)
            if module:
                module_codes.append(module.code)
        highlight_modules(G, plot, graph_renderer, module_codes)
    elif search_term:
        matched_modules = search_keywords(search_term)
        if matched_modules:
            module_codes = [module['module_code'] for module in matched_modules]
            highlight_modules(G, plot, graph_renderer, module_codes)
    else:
        highlight_modules(G, plot, graph_renderer, [])

    with open("modules_network.html", "r") as f:
        html_content = f.read()

    return render(request, 'modules/module_graph.html', {
        'html_content': html_content,
        'modules': get_modules(),
        'choose_modules': choose_modules,
        'search_term': search_term
    })

def module_detail(request, module_code):
    module = get_module_by_code(get_long_module_code(module_code))
    append_module_info(module)
    assessments = Assessment.objects.filter(module_name=module.name)
    return render(request, 'modules/module_detail.html', {'module': module, 'assessments': assessments})