import importlib
import logging
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone
from api.serializer.fields import CustomDateTimeField, CustomDateField, CustomTimeField, CustomManyRelatedField


# * ------------------------- App Serializer Generator ------------------------- * #

logger = logging.getLogger(__name__)


    

class AppSerializer(serializers.ModelSerializer):
    exclude = ['password', 'last_login']
    list_display_links = ['id']
    read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined']
    depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_fields = [field.name for field in self.Meta.model._meta.get_fields()]
        self.exclude = [field for field in self.exclude if field in self.valid_fields and field]

        for field_name, field in self.fields.items():
            if isinstance(field, serializers.DateTimeField):
                self.fields[field_name] = CustomDateTimeField()
            elif isinstance(field, serializers.DateField):
                self.fields[field_name] = CustomDateField()
            elif isinstance(field, serializers.TimeField):
                self.fields[field_name] = CustomTimeField()
            # elif isinstance(field, serializers.ManyRelatedField):
            #     self.fields[field_name] = CustomManyRelatedField(self)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        return representation

    class Meta:
        model = None


def generate_serializer(model_class):
    if hasattr(model_class, 'serializer_class'):
        serializer_class_path = getattr(model_class, 'serializer_class')
        if isinstance(serializer_class_path, str):
            module_name, class_name = serializer_class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            custom_serializer_class = getattr(module, class_name)
            return custom_serializer_class

    class GenericSerializer(AppSerializer):
        class Meta:
            model = model_class
            exclude = AppSerializer.exclude

    return GenericSerializer
