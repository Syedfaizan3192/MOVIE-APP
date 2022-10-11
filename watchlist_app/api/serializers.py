from dataclasses import fields
from multiprocessing.sharedctypes import Value
from platform import platform
from wsgiref import validate
from rest_framework import serializers
from watchlist_app import models
from watchlist_app.models import WatchList, StremVideos, Review


# def name_len(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Try Again Not valid")
#     return value


# serializer.ModelSerializer


class Rviewserializers(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('WatchList',)
        # fields = "__all__"


class WatchListserializers(serializers.ModelSerializer):
    # Review = Rviewserializers(many=True, read_only=True)
    # To get platform name:
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"


class StremVideosSerializers(serializers.ModelSerializer):

    watchlist = WatchListserializers(many=True, read_only=True)

    class Meta:
        model = StremVideos
        fields = "__all__"


# Serializer.Serializer

# class Movieserializers(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_len])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movies.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

    # Validation - Field validation

    # ...............................................

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Not a valid!")
    #     return value

    # Validation - object validation
    # ...............................................

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Not a valid!")
    #     return data
