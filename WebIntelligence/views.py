from django.shortcuts import render
from django.apps import apps


def index(request):
    app_names = []
    for app_conf in apps.get_app_configs():
        if not app_conf.name.startswith('django'):
            app_names.append(app_conf.name)

    return render(request, './index.html', {'apps': app_names})
