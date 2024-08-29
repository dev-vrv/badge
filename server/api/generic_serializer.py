import importlib
import logging
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone
logger = logging.getLogger(__name__)

FIELDS_MAP = {
    'number': [
        'AutoField', 
        'BigAutoField', 
        'BigIntegerField', 
        'DecimalField', 
        'FloatField', 
        'IntegerField', 
        'PositiveIntegerField', 
        'PositiveSmallIntegerField', 
        'SmallIntegerField'
    ],
    'textarea': [
        'BinaryField',
        'TextField',
        'JSONField',
        'XMLField',
        'YAMLField',
    ],
    'text': [
        'CharField', 
        'SlugField', 
        'URLField',    
    ],
    'date': [
        'DateField',
    ],
    'datetime': [
        'DateTimeField',  
    ],
    'time': [
        'DurationField',
        'TimeField',
    ],
    'checkbox': [
        'BooleanField',
    ],
    'email': [
        'EmailField',
    ]
}


class AppSerializer(serializers.ModelSerializer):
    exclude = ['password', 'last_login']
    list_display_links = ['id']
    read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valid_fields = [field.name for field in self.Meta.model._meta.get_fields()]
        self.exclude = [field for field in self.exclude if field in valid_fields and field]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for field_name, field in self.fields.items():
            value = representation.get(field_name)
            if value:
                try:
                    if isinstance(field, serializers.DateTimeField):
                        dt_value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                        aware_dt_value = dt_value.replace(tzinfo=dt_timezone.utc)
                        representation[field_name] = timezone.localtime(aware_dt_value).strftime('%d.%m.%Y %H:%M')
                    elif isinstance(field, serializers.DateField):
                        date_value = datetime.strptime(value, '%d.%m.%Y').date()
                        representation[field_name] = date_value.strftime('%d.%m.%Y')
                    elif isinstance(field, serializers.TimeField):
                        time_value = datetime.strptime(value, '%H:%M:%S').time()
                        representation[field_name] = time_value.strftime('%H:%M')
                except Exception as e:
                    logging.error(f'Error in {self.Meta.model} serializer: {e}')

        return representation
    
    class Meta:
        model = None

    
def _collect_field_metadata(model, instance=None, exclude_fields=None):
    field_metadata = []
    for field in model._meta.get_fields():
        if exclude_fields and field.name in exclude_fields:
            continue
        
        if isinstance(field, models.Field):
            field_type = [k for k, v in FIELDS_MAP.items() if type(field).__name__ in v]
            field_info = {
                'list_display_link': field.name in AppSerializer.list_display_links,
                'name': field.name,
                'type': field_type[0] if field_type else None,
                'readonly': field.name in AppSerializer.read_only_fields,
                'null': getattr(field, 'null', None),
                'blank': getattr(field, 'blank', None),
                'value': getattr(instance, field.name) if instance else None,
                'max_length': field.max_length if hasattr(field, 'max_length') else None,
            }
            field_metadata.append(field_info)

    return field_metadata

def get_instance_metadata(instance):
    model = instance.__class__
    return _collect_field_metadata(model, instance=instance)

def get_fields_metadata(model, serializer):
    exclude = serializer.exclude
    return _collect_field_metadata(model, exclude_fields=exclude)


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