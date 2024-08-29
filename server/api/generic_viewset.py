from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class ApiViewSet(viewsets.ViewSet):

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    
    
    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        obj = self.queryset.get(pk=pk)
        return Response(self.serializer_class(obj).data)

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
