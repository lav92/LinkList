from rest_framework import serializers
from django.contrib.auth.models import User

from links.models import Link, Collection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email']


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        read_only_fields = ['pk', ]
        fields = ['pk', 'title', 'short_description', 'url', 'type',]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        read_only_fields = ['pk', ]
        fields = ['pk', 'title', 'short_description',]
