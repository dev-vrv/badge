import logging
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action 
from django.shortcuts import get_object_or_404

# * ------------------------- App ViewSet Generator ------------------------- * #

logger = logging.getLogger(__name__)


class ApiViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'], url_path='list')
    def get_list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='detail')
    def get_detail(self, request, pk=None):
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='update')
    def set_update(self, request, pk=None):
        data = request.data
        obj = self.queryset.get(pk=pk)
        serializer = self.serializer_class(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


def generate_viewset(model_obj, serializer_cls):
    class GenericViewSet(ApiViewSet):
        model = model_obj
        queryset = model.objects.all()
        serializer_class = serializer_cls    
    return GenericViewSet
