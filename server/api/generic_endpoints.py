from .generic_serializer import generate_serializer, get_fields_metadata
from .generic_viewset import generate_viewset
from django.apps import apps
from django.conf import settings

import re
import logging

logger = logging.getLogger(__name__)
apps_list = settings.INSTALLED_APPS_API


def clean_url(patterns):
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


def clean_pattern_name(name):
    name = name.split('-')
    return name[-1]


def generic_apps_endpoints(apps_list: list[str]):
    generic = []
    for app in apps_list:
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


def generic_apps_configs(router, model, serializer) -> dict:
    generated_paths_info = {}
    
    app_label = model._meta.app_label
    model_name = model._meta.model_name

    if app_label not in generated_paths_info:
        generated_paths_info[app_label] = {}

    if model_name not in generated_paths_info[app_label]:
        generated_paths_info[app_label][model_name] = {
            'endpoints': {},
            'fields': get_fields_metadata(model, serializer),
        }

    for url_pattern in router.urls:
        name = url_pattern.name
        app_path = f'{app_label}/{model_name}'
        patterns = str(url_pattern.pattern)

        if app_path in patterns and not "\\.(?P<format>[a-z0-9]+)" in patterns:
            endpoints = generated_paths_info[app_label][model_name]['endpoints']
            if name not in endpoints:
                endpoints[clean_pattern_name(name)] = {
                    'endpoint': clean_url(patterns),
                    'method': 'GET',
                }

    return generated_paths_info