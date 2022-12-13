import datetime

from drf_spectacular.utils import extend_schema

from rest_framework import generics, status
from rest_framework.response import Response

from space import serializers, models


@extend_schema(description='View model instances ', methods=["GET"])
@extend_schema(description='Create model instance', methods=["POST"])
class SpaceStationListCreateApiView(generics.ListCreateAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer

    def perform_create(self, serializer):
        serializer.save(position_x=100, position_y=100, position_z=100)


@extend_schema(description='Retrieve model instance ', methods=["GET"])
@extend_schema(description='Update model instance name', methods=["PUT"])
@extend_schema(description='Update model instance name', methods=["PATCH"])
@extend_schema(description='Delete model instance', methods=["DELETE"])
class SpaceStationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SpaceStation.objects.all()
    serializer_class = serializers.SpaceStationSerializer


@extend_schema(
    request=serializers.PointingSerializer,
    responses={200: serializers.SpaceStationStateSerializer},
    methods=["POST"]
)
@extend_schema(description='Retrieving instance XYZ positions ', methods=["GET"])
@extend_schema(description='Creating new pointing with overrided response - instance XYZ positions',
               methods=["POST"])
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
            obj.position_z += distance
            value = obj.position_z
        if value < 0:
            obj.condition = "broken"
            obj.date_broken = datetime.datetime.today()
        obj.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        pk = self.kwargs['pk']
        instance = models.SpaceStation.objects.get(pk=pk)
        serializer = serializers.SpaceStationStateSerializer(instance)
        return Response(serializer.data)
