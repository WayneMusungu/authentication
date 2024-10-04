from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from drones.models import Drone
from drones.serializers import DroneSerializer
from rest_framework.throttling import UserRateThrottle

class DroneListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.drones.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class DroneRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.drones.all()

    