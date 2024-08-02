from django.urls import path

from drones.views import DroneListCreate, DroneRetrieveUpdateDestroy

urlpatterns = [
    path('drones/', DroneListCreate.as_view(), name='list-create-api'),
    path('drones/<int:pk>', DroneRetrieveUpdateDestroy.as_view(), name='retrieve-update-destroy-api'),
]