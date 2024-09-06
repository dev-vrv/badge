from django.db import models
from api.gen.serializer import AppSerializer


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
    ],
    'selected': [
        'ForeignKey',
        'OneToOneField',
    ],
    'related': [
        'ManyToManyField',
    ]
}

    
def _detect_field_type(field):
    if hasattr(field, 'choices') and field.choices:
        return 'selected'
    
    field_type = [k for k, v in FIELDS_MAP.items() if type(field).__name__ in v]
    return field_type[0] if field_type else None


def _detect_field_choices(field, instance=None):
    result = None
    if hasattr(field, 'choices') and field.choices:
        if instance is None:
            result = list(field.choices)
        else:
            display_method = f"get_{field.name}_display"
            if hasattr(instance, display_method):
                result =  getattr(instance, display_method)()
    if isinstance(field, (models.ForeignKey, models.ManyToManyField, models.OneToOneField)):
        result = list(field.related_model.objects.values_list('id', 'name'))
    if instance is not None:
        result =  getattr(instance, field.name)

    return result

    
def _collect_field_metadata(model, instance=None, exclude_fields=None):
    field_metadata = []
    for field in model._meta.get_fields():
        if exclude_fields and field.name in exclude_fields:
            continue
        
        if isinstance(field, models.Field):
            field_info = {
                'name': field.name,
                'type': _detect_field_type(field),
                'list_display_link': field.name in AppSerializer.list_display_links,
                'max_length': field.max_length if hasattr(field, 'max_length') else None,
                'readonly': field.name in AppSerializer.read_only_fields,
                'blank': getattr(field, 'blank', None),
                'choices': _detect_field_choices(field, instance),
            }
            field_metadata.append(field_info)

    return field_metadata


def get_instance_metadata(instance):
    model = instance.__class__
    return _collect_field_metadata(model, instance=instance)


def get_fields_metadata(model, serializer):
    exclude = serializer.exclude
    return _collect_field_metadata(model, exclude_fields=exclude)
