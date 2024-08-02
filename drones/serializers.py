from drones.models import Drone
from rest_framework import serializers


class DroneSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Drone
        fields = ['id', 'name', 'description', 'price', 'user']
     
