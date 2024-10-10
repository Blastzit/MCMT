import sqlite3
from django.shortcuts import render
from modules.utils import *
from modules.models import Assessment, Module
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from icalendar import Calendar, Event
from datetime import timedelta
from fuzzywuzzy import process
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

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

# Dash app 
app = DjangoDash('assessment_calendar')

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='module-dropdown', 
        options=[
            {'label': module.name, 'value': module.name} 
            for module in Module.objects.all()
        ], 
        multi=True, 
        placeholder="Select modules",
    ),
    dcc.Graph(id='calendar-graph'),
    html.Button("Export to Outlook Calendar", id="export-button", n_clicks=0),
    html.Div(id="outlook-export-link"),
])

# update calendar 
@app.callback(
    Output('calendar-graph', 'figure'),
    [Input('module-dropdown', 'value')]
)
def update_calendar(selected_modules):
    if selected_modules:
        assessments = Assessment.objects.filter(module_name__in=selected_modules)
    else:
        assessments = Assessment.objects.all()

    # Generate events
    events = []
    for assessment in assessments:
        events.append(dict(
            x=[assessment.start_date, assessment.end_date],
            y=[assessment.module_name, assessment.module_name],
            name=assessment.coursework_name,
        ))

    # plot 
    fig = go.Figure()

    for event in events:
        fig.add_trace(go.Scatter(
            x=event['x'], 
            y=event['y'], 
            mode='lines+markers', 
            name=event['name']
        ))

    fig.update_layout(title="Coursework Calendar", height=600, width=900)
    return fig

# Export to Outlook 
@app.callback(
    Output("outlook-export-link", "children"),
    [Input("export-button", "n_clicks")],
    [Input('module-dropdown', 'value')]
)
def export_outlook(n_clicks, selected_modules):
    if n_clicks > 0:
        assessments = Assessment.objects.filter(module_name__in=selected_modules)

        cal = Calendar()
        cal.add('prodid', '-//MCMT Coursework Calendar//')
        cal.add('version', '2.0')

        for assessment in assessments:
            event = Event()
            event.add('summary', assessment.coursework_name)
            event.add('dtstart', assessment.start_date)
            event.add('dtend', assessment.end_date + timedelta(days=1))
            event.add('description', f'Module: {assessment.module_name}')
            event.add('location', 'Submit via: ' + assessment.submit_work_to)
            cal.add_component(event)

        ics_data = cal.to_ical().decode('utf-8')
        outlook_link = f'<a href="data:text/calendar;charset=utf-8,{ics_data}" download="coursework_calendar.ics">Download Calendar</a>'
        return outlook_link
    return ""
##degree tab
degree_descriptions = {
    "G100": "G100 Mathematics (BSc)",
    "G102": "G102 Mathematics with Mathematical Computation",
    "G103": "G103 Mathematics (MSci)",
    "G104": "G104 Mathematics with a Year Abroad (MSci)",
    "G125": "G125 Mathematics (Pure Mathematics)",
    "G1F3": "G1F3 Mathematics with Applied Mathematics/Mathematical Physics",
    "G1G3": "G1G3 Mathematics with Statistics",
    "G1GH": "G1GH Mathematics with Statistics for Finance",
    "GG31": "GG31 Mathematics, Optimisation and Statistics"
}

group_names = {
    "Year 1": ["modules"],
    "Year 2": ["group_a", "group_b", "compulsory_modules"],
    "Year 3": ["modules"],
    "Year 4": ["modules"],
}

def get_degree_modules(degree, year):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    degree_modules = {}

    for group in group_names[year]:
        if year == 'Year 4':
            cursor.execute("""
                SELECT modules FROM degree_group
                WHERE degree_code = ? AND (year = 'Year 3' OR year = 'Year 4') AND group_name = ?
            """, (degree, group))
        else:
            cursor.execute("""
                SELECT modules FROM degree_group
                WHERE degree_code = ? AND year = ? AND group_name = ?
            """, (degree, year, group))

        results = cursor.fetchall()

        if not results:
            continue

        for i, result in enumerate(results):
            modules = result[0].split(',')

            processed_modules = []
            for module in modules:
                module = module.strip()
                module_obj = None
                if module.startswith('MATH') and module[4].isdigit():
                    module_obj = get_module_by_code(module)
                else:
                    module_obj = get_module_by_name(module)
                if module_obj:
                    append_module_info(module_obj)
                    processed_modules.append(module_obj)

            if year == 'Year 4':
                degree_modules[f'year_{i + 3}_modules'] = processed_modules
            else:
                degree_modules[group] = processed_modules

    conn.close()
    return degree_modules

def get_degree_guideline(degree, year):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT guideline FROM degree_guide
        WHERE degree_code = ? AND year = ?
    """, (degree, year))

    result = cursor.fetchone()
    conn.close()

    if not result:
        return ""

    return result[0]

def get_fuzzy_matches(query, module_list, limit=5):
    return process.extract(query, module_list, limit=limit)

def degree_view(request):
    selected_description = request.GET.get('degree', list(degree_descriptions.values())[0])
    degree = {v: k for k, v in degree_descriptions.items()}.get(selected_description, "")
    year = request.GET.get('year', 'Year 2')
    search_query = request.GET.get('search', '')

    degree_info = get_degree_modules(degree, year)
    guideline = get_degree_guideline(degree, year)

    modules = degree_info.get('modules', [])
    group_a_modules = degree_info.get('group_a', [])
    group_b_modules = degree_info.get('group_b', [])

    combined_modules = modules + group_a_modules + group_b_modules
    module_names = [module.name for module in combined_modules]

    fuzzy_suggestions = []

    if search_query:
        fuzzy_suggestions = get_fuzzy_matches(search_query, module_names)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'fuzzy_suggestions': fuzzy_suggestions,
        })

    context = {
        'degree_descriptions': degree_descriptions,
        'selected_description': selected_description,
        'degree': degree,
        'year': year,
        'degree_info': degree_info,
        'guideline': guideline,
        'fuzzy_suggestions': fuzzy_suggestions,
        'search_query': search_query
    }

    return render(request, 'degree.html', context)
#Our team
def our_team_view(request):
    return render(request, 'our_team.html')