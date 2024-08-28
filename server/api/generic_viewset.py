from rest_framework import viewsets

def generate_viewset(model, serializer_cls):
    class GenericViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer_cls    
    return GenericViewSet
