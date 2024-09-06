import re
import logging
from .serializer import generate_serializer
from .viewset import generate_viewset
from api.meta.fields import get_fields_metadata
from django.apps import apps
from django.conf import settings


# * ------------------------- App ViewSet Generator ------------------------- * #

logger = logging.getLogger(__name__)

class EndpointsGenerator:
    def __init__(self):
        self.apps = settings.INSTALLED_APPS_API
        self.endpoints = None
        self.apps_configs = None
           
    def clean_pattern_name(self, name: str) -> str:
        name = name.split('-')
        return name[-1]
            
    def clean_url(self, patterns: str) -> str:
        url = re.sub(r'\(\?P<[^)]+>\[[^]]+\]\+\)', '', patterns)
        url = re.sub(r'\(\?P<\w+>[a-z0-9]+\)/?', '', url)
        url = url.replace('^', '').replace('$', '')
        url = url.replace('\\\\', '') 
        url = url.strip('/')
        url = url.replace('(?P<pk>[/.]+)', '')
        url = url.replace('(?P<pk>[a-z0-9]+)', '')
        if not url.endswith('/'):
            url += '/'
        return '/api/' + url
    
    def generate_endpoints(self):
        generic = []
        for app in self.apps:
            try:
                app_config = apps.get_app_config(app)
                models = app_config.get_models()

                for model in models:
                    serializer = generate_serializer(model)
                    viewset = generate_viewset(model, serializer)
                    generic.append((model, serializer, viewset))

            except Exception as e:
                logging.error(f'Generic Api Error in {app} app: {e}')
        return generic

    def generic_apps_configs(self, router, model, serializer) -> dict:
        self.apps_configs = {}
        
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        if app_label not in self.apps_configs:
            self.apps_configs[app_label] = {}

        if model_name not in self.apps_configs[app_label]:
            self.apps_configs[app_label][model_name] = {
                'endpoints': {},
                'fields': get_fields_metadata(model, serializer),
            }

        for url_pattern in router.urls:
            name = url_pattern.name
            app_path = f'{app_label}/{model_name}'
            patterns = str(url_pattern.pattern)
            if app_path in patterns and not "\\.(?P<format>[a-z0-9]+)" in patterns:
                endpoints = self.apps_configs[app_label][model_name]['endpoints']
                if name not in endpoints:
                    endpoints[self.clean_pattern_name(name)] = {
                        'endpoint': self.clean_url(patterns),
                        'method': 'GET',
                    }
        return self.apps_configs
            


