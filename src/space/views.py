import datetime

from rest_framework import generics
from rest_framework.response import Response

from space import serializers, models


class SpaceStationListCreateApiView(generics.ListCreateAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer

    def perform_create(self, serializer):
        serializer.save(position_x=100, position_y=100, position_z=100)


class SpaceStationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer


class SpaceStationStateRetrieveCreateAPIView(generics.RetrieveAPIView, generics.CreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SpaceStationStateSerializer
        else:
            return serializers.PointingSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.SpaceStation.objects.all()
        else:
            return models.Pointing.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        pk = self.kwargs['pk']
        axis = self.request.data['axis']
        distance = int(self.request.data['distance'])
        obj = models.SpaceStation.objects.get(pk=pk)
        if axis == 'x':
            obj.position_x += distance
            value = obj.position_x
        elif axis == "y":
            obj.position_y += distance
            value = obj.position_y
        else:
            obj.position_z = +distance
            value = obj.position_z
        if value < 0:
            obj.condition = "broken"
            obj.date_broken = datetime.datetime.today()
        obj.save()
