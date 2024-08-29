from api.generic_serializer import AppSerializer
from .models import Users

class AppUsersSerializer(AppSerializer):
    class Meta:
        model = Users
        exclude = ['id', 'email'] + AppSerializer.exclude