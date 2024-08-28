import logging
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone


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
    'string': [
        'CharField', 
        'EmailField', 
        'SlugField', 
        'TextField', 
        'URLField',    
    ],
    'date': [
        'DateField',
        'DateTimeField',
        'TimeField',
    ],
    'boolean': [
        'BooleanField',
    ],
}

logger = logging.getLogger(__name__)


class AppSerializer(serializers.ModelSerializer):
    exclude_fields = ['password', 'last_login']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valid_fields = [field.name for field in self.Meta.model._meta.get_fields()]
        self.exclude_fields = [field for field in self.exclude_fields if field in valid_fields and field]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Форматирование дат и времени
        for field_name, field in self.fields.items():
            value = representation.get(field_name)
            
            if value:
                try:
                    if isinstance(field, serializers.DateTimeField):
                        dt_value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                        aware_dt_value = dt_value.replace(tzinfo=dt_timezone.utc)
                        representation[field_name] = timezone.localtime(aware_dt_value).strftime('%Y-%m-%d %H:%M')
                    elif isinstance(field, serializers.DateField):
                        date_value = datetime.strptime(value, '%Y-%m-%d').date()
                        representation[field_name] = date_value.strftime('%Y-%m-%d')
                    elif isinstance(field, serializers.TimeField):
                        time_value = datetime.strptime(value, '%H:%M:%S').time()
                        representation[field_name] = time_value.strftime('%H:%M')
                except Exception as e:
                    logging.error(f'Error in {self.Meta.model} serializer: {e}')
                    print(e)
        
        return representation
def get_instance_metadata(instance):
    model = instance.__class__
    field_metadata = []
    
    for field in model._meta.get_fields():
        if isinstance(field, models.Field):
            field_type = [k for k, v in FIELDS_MAP.items() if type(field).__name__ in v]
            field_info = {
                'name': field.name,
                'type': field_type[0] if field_type else None,
                'value': getattr(instance, field.name),
                'null': getattr(field, 'null', None),
                'blank': getattr(field, 'blank', None),
                'readonly': not field.editable,
            }

            if hasattr(field, 'max_length'):
                field_info['max_length'] = field.max_length

            field_metadata.append(field_info)
    
    return field_metadata


def get_fields_metadata(model, serializer):
    field_metadata = []
    exclude = serializer.exclude_fields

    for field in model._meta.get_fields():
        if field.name in exclude:
            continue
        
        if isinstance(field, models.Field):
            field_type = [k for k, v in FIELDS_MAP.items() if type(field).__name__ in v]
            field_info = {
                'name': field.name,
                'type': field_type[0] if field_type else None,
                'null': getattr(field, 'null', None),
                'blank': getattr(field, 'blank', None),
                'readonly': not field.editable,
            }

            if hasattr(field, 'max_length'):
                field_info['max_length'] = field.max_length

            field_metadata.append(field_info)
    return field_metadata


def generate_serializer(model_class):
    class GenericSerializer(AppSerializer):
        class Meta:
            model = model_class
            exclude = AppSerializer.exclude_fields
    
    return GenericSerializer