import importlib
import logging
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone
from django.contrib.auth.models import Permission, Group
from api.serializer.fields import (
    CustomDateTimeField, 
    CustomDateField, 
    CustomTimeField, 
    CustomManyRelatedField, 
)

# * ------------------------- App Serializer Generator ------------------------- * #

logger = logging.getLogger(__name__)


class AppSerializer(serializers.ModelSerializer):
    exclude = ['password', 'last_login']
    list_display_links = ['id']
    read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_fields = [field.name for field in self.Meta.model._meta.get_fields()]

        self.exclude = [field for field in self.exclude if field in self.valid_fields]

        self.Meta.exclude = self.exclude

        for field_name, field in self.fields.items():

            if isinstance(field, serializers.DateTimeField):
                self.fields[field_name] = CustomDateTimeField()
            elif isinstance(field, serializers.DateField):
                self.fields[field_name] = CustomDateField()
            elif isinstance(field, serializers.TimeField):
                self.fields[field_name] = CustomTimeField()
            elif isinstance(field, serializers.ManyRelatedField):
                related_model = self.Meta.model._meta.get_field(field_name).related_model
                self.fields[field_name] = CustomManyRelatedField(queryset=related_model.objects.all())


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    
    def _get_nested_serializer(self, related_model):
        class NestedSerializer(serializers.ModelSerializer):
            class Meta:
                model = related_model
                fields = '__all__'

        return NestedSerializer()


    class Meta:
        model = None
        fields = '__all__'

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
