from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from drones.models import Drone
from drones.serializers import DroneSerializer


class DroneListCreate(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return user.drones.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class DroneRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return user.drones.all()

    