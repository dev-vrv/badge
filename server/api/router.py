from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .generic_endpoints import generic_apps_endpoints, generic_apps_configs
import logging

logger = logging.getLogger(__name__)
router = DefaultRouter()

apps_list = settings.INSTALLED_APPS_API
endpoints = generic_apps_endpoints(apps_list)

configs = []
for model, serializer, viewset in endpoints:
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    endpoint = rf'{app_label}/{model_name}'
    
    router.register(endpoint, viewset, basename=f'{app_label}-{model_name}')
    
    configs.append(generic_apps_configs(router, model, serializer)) 
    
    logger.info(f"Registered endpoint: {endpoint}")
    

class GeneratedEndpointsView(APIView):
    def get(self, request):
        generated_paths_info = {}

        for model, serializer, viewset in endpoints:            
            app_info = generic_apps_configs(router, model, serializer)
            generated_paths_info.update(app_info)

        return Response(generated_paths_info)