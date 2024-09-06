import importlib
import logging
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone


# * ------------------------- App Serializer Generator ------------------------- * #

logger = logging.getLogger(__name__)

class AppSerializer(serializers.ModelSerializer):
    exclude = ['password', 'last_login']
    list_display_links = ['id']
    read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valid_fields = [
            field.name for field in self.Meta.model._meta.get_fields()]
        self.exclude = [
            field for field in self.exclude if field in valid_fields and field]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for field_name, field in self.fields.items():
            value = representation.get(field_name)
            if value:
                try:
                    if isinstance(field, serializers.DateTimeField):
                        dt_value = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%S.%fZ')
                        aware_dt_value = dt_value.replace(
                            tzinfo=dt_timezone.utc)
                        representation[field_name] = timezone.localtime(
                            aware_dt_value).strftime('%d.%m.%Y %H:%M')
                    elif isinstance(field, serializers.DateField):
                        date_value = datetime.strptime(
                            value, '%d.%m.%Y').date()
                        representation[field_name] = date_value.strftime(
                            '%d.%m.%Y')
                    elif isinstance(field, serializers.TimeField):
                        time_value = datetime.strptime(
                            value, '%H:%M:%S').time()
                        representation[field_name] = time_value.strftime(
                            '%H:%M')
                except Exception as e:
                    logging.error(
                        f'Error in {self.Meta.model} serializer: {e}')

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
