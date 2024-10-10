def tabs(request):
    return {
        'tabs': [
            {"name": "Modules", "url": "/modules/"},
            {"name": "Assessments", "url": "/assessment/"},
            {"name": "Degree", "url": "/degree/"},
            {"name": "Careers", "url": "/careers/"},
        ]
    }