from django.urls import path, include
from .router import router, GeneratedEndpointsView


urlpatterns = [
    path('', include(router.urls)),
    path('endpoints/', GeneratedEndpointsView.as_view(), name='endpoints'),
]
    