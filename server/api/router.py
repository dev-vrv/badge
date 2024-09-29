from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from api.gen.endpoints import EndpointsGenerator
import logging

logger = logging.getLogger(__name__)
router = DefaultRouter()
generator = EndpointsGenerator()
endpoints = generator.generate_endpoints()

configs = []
for model, serializer, viewset in endpoints:
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    endpoint = rf'{app_label}/{model_name}'
    
    router.register(endpoint, viewset, basename=f'{app_label}-{model_name}')
    
    configs.append(generator.generic_apps_configs(router, model, serializer, viewset)) 
    
    logger.info(f"Registered endpoint: {endpoint}")
    



class GeneratedEndpointsView(APIView):
    def get(self, request):
        generated_paths_info = {}

        for model, serializer, viewset in endpoints:            
            app_info = generator.generic_apps_configs(router, model, serializer)
            generated_paths_info.update(app_info)

        return Response(generated_paths_info)
    