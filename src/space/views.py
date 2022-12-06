from rest_framework import generics

from space import serializers, models
class SpaceStationListCreateApiView(generics.ListCreateAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer

    def perform_create(self, serializer):
        serializer.save(position_x=100,position_y=100,position_z=100)



class SpaceStationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer


class SpaceStationStatusRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationStatusSerializer
