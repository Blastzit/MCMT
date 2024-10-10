from .models import Module
from django.db import connections
from fuzzywuzzy import fuzz

def get_modules():
    modules = Module.objects.values_list('name', flat=True)
    return list(modules)

def get_module_by_code(module_code):
    try:
        module = Module.objects.get(code=module_code)
        return module
    except Module.DoesNotExist:
        return None

def get_module_by_name(module_name):
    try:
        module = Module.objects.get(name=module_name)
        return module
    except Module.DoesNotExist:
        return None

def get_modules_by_year():
    # ideally this should also return term, so no need for extra search later

    modules = Module.objects.all().order_by('code')

    modules_by_year = {
        'Year 1': [],
        'Year 2': [],
        'Year 3': [],
        'Year 4': []
    }
    for module in modules:
        append_module_info(module)
        modules_by_year[f'Year {module.year}'].append(module)

    return modules_by_year

def append_module_info(module):
    module.year = int(module.code[4]) - 3 if module.code[4].isdigit() else 1
    module.short_code = get_short_module_code(module.code)
    if module.year == 1 or (module.year == 2 and '/' in module.code):
        module.compulsory = True
    else:
        module.compulsory = False   
    
    if module.learning_outcome and isinstance(module.learning_outcome, str):
        outcomes = module.learning_outcome.replace('\r\n', ' ').split(';')
        outcomes = [item.strip() for item in outcomes]
        module.learning_outcome = outcomes

def get_short_module_code(module_code):
    if module_code == 'MATH40001':
        return 'IUM'
    if module_code[4] == '6':
        return module_code.replace('/', '_').replace('MATH', 'M')[:6]
    return module_code.replace('/', '_').replace('MATH', 'M')

def get_long_module_code(module_code):
    if module_code == 'IUM':
        return 'MATH40001'
    if module_code[1] == '6':
        return f'MATH{module_code[1:]}/7{module_code[2:]}'
    return module_code.replace('_', '/').replace('M', 'MATH')

def search_keywords(search_term):
    with connections['keywords'].cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        matched_results = []

        for table in tables:
            module_code = table[0]
            query = f'SELECT * FROM "{module_code}"'
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                keyword = row[2]
                broad_topic = row[1] if row[1] else "N/A"
                match_score = fuzz.partial_ratio(search_term.lower(), keyword.lower())
                if match_score >= 80:
                    matched_results.append({
                        'module_code': get_long_module_code(module_code),
                        'broad_topic': broad_topic,
                        'keyword': keyword
                    })
        return matched_results