from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.urls import include, path
from server.urls import urlpatterns

@receiver(post_migrate)
def register_dynamic_urls(sender, **kwargs):
    urlpatterns.append(path('api/', include('api.urls')))