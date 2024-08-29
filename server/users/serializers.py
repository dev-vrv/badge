from api.generic_serializer import AppSerializer
from .models import Users

class AppUsersSerializer(AppSerializer):
    class Meta:
        model = Users
        exclude = [] + AppSerializer.exclude
        read_only_fields = [] + AppSerializer.read_only_fields