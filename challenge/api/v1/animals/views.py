from decimal import Decimal

from copy import copy

from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response

from animals.models import Animal, Herd, WeightEntry
from .serializers import AnimalSerializer, DatetimeSerializer, HerdSerializer, WeightEntrySerializer


class AnimalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Animal objects
    """
    lookup_field = 'pid'
    lookup_url_kwarg = 'pid'
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    # list: all with details
    @action(methods=['post'], detail=False)
    def total_weight(self, request):
        """
        Calculate the total animals weight for a given point in time.
        """
        serializer = DatetimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        counted = 0
        total_weight = Decimal(0.00)
        for animal in Animal.objects.all():
            animal_weight = animal.calculate_weight(serializer.validated_data['datetime'])
            if animal_weight:
                total_weight += animal_weight
                counted += 1

        if counted != 0:
            total_weight = round(total_weight / counted, 2)

        return Response({'total_weight': total_weight})

    @action(methods=['post'], detail=True)
    def add_weight(self, request, pid=None):
        """
        Add a weight entry for the detail Animal.

        :raises: NotFound when the Animal is not found.
        """
        animal = self.get_object()

        data = copy(request.data)
        data['animal'] = animal.id
        serializer = WeightEntrySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = AnimalSerializer(animal)
        return Response(serializer.data)


class WeightEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for WeightEntry objects
    """
    queryset = WeightEntry.objects.all()
    serializer_class = WeightEntrySerializer
    # add a weith_entry


class HerdViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Herd objects
    """
    lookup_field = 'pid'
    lookup_url_kwarg = 'pid'
    queryset = Herd.objects.all()
    serializer_class = HerdSerializer

    @action(methods=['post'], detail=True)
    def add_animal(self, request, pid=None):
        """
        Add a given Animal to the detail Herd.

        :raises: NotFound when the Animal or Herd are not found.
        """
        herd = self.get_object()
        animal_pid = request.data.get('animal_pid')
        try:
            animal = Animal.objects.get(pid=animal_pid)
        except Animal.DoesNotExist:
            raise NotFound('Animal does not exist')

        herd.animals.add(animal)
        serializer = HerdSerializer(herd)
        return Response(serializer.data)
