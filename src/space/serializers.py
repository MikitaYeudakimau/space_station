from rest_framework import serializers

from space import models


class SpaceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpaceStation
        fields = ['id', 'name', 'position_x', 'position_y', 'position_z', 'condition', 'date_creation', 'date_broken']
        extra_kwargs = {
            'date_broken': {
                'required': False,
            },
        }
        read_only_fields = ['condition', 'position_x', 'position_y', 'position_z', 'date_creation', 'date_broken']



class SpaceStationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpaceStation
        fields = ['position_x', 'position_y', 'position_z']


class PointingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pointing
        fields = ['axis', 'distance','user']
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
        }