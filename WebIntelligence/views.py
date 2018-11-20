from django.apps import apps
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'apps'

    def get_queryset(self):
        app_names = []
        for app_conf in apps.get_app_configs():
            if not app_conf.name.startswith('django'):
                app_names.append(app_conf.name)
        return app_names
