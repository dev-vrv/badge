import logging
from rest_framework import serializers
from django.db import models


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


def get_fields_metadata(model, exclude=None):
    field_metadata = []
    exclude = exclude or []

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


def generate_serializer(model_class, exclude=None):
    exclude = exclude or []

    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            exclude = ['password']

    return GenericSerializer
