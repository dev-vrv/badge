from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class ApiViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)
    

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

def generate_viewset(model_obj, serializer_cls):
    class GenericViewSet(ApiViewSet):
        model = model_obj
        queryset = model.objects.all()
        serializer_class = serializer_cls    
    return GenericViewSet
