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



class CustomManyRelatedField(serializers.ManyRelatedField):
    def to_representation(self, value):

        related_serializer = self.child_relation
        print('related_serializer', related_serializer)
        return []