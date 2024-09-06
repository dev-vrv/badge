from rest_framework import serializers
from django.utils import timezone

class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if value:
            value = timezone.localtime(value).strftime('%d.%m.%Y %H:%M:%S')
            return value
        return super().to_representation(value)

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime('%d.%m.%Y')
        return super().to_representation(value)

class CustomTimeField(serializers.TimeField):
    def to_representation(self, value):
        if value:
            return value.strftime('%H:%M')
        return super().to_representation(value)


class CustomManyRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if hasattr(value, 'all'):
            current_relations = [self._get_representation(item) for item in value.all()]
        else:
            current_relations = [self._get_representation(value)]
        return current_relations

    def _get_representation(self, item):
        return {
            'id': item.id,
            'name': str(item),
        }

    def get_queryset(self):
        related_model = self.queryset.model
        return related_model.objects.all()