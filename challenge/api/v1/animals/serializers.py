from rest_framework import serializers

from animals.models import Animal, Herd, WeightEntry


class WeightEntrySerializer(serializers.ModelSerializer):
    """
    WeightEntry serializer.
    """
    class Meta:
        model = WeightEntry
        fields = ('animal', 'weight', 'weigh_datetime')


class AnimalWeightEntrySerializer(serializers.ModelSerializer):
    """
    WeightEntry serializer for a particular Animal (animal details excluded)
    """
    class Meta:
        model = WeightEntry
        fields = ('weight', 'weigh_datetime')


class AnimalSerializer(serializers.ModelSerializer):
    """
    Animal serializer, listing the wight entries details.
    """
    weight_entries = AnimalWeightEntrySerializer(read_only=True, many=True, source='get_weight_entries')

    class Meta:
        model = Animal
        fields = ('pid', 'herd', 'weight_entries')


class HerdSerializer(serializers.ModelSerializer):
    """
    Herd serializer, listing all animals with their weight entries.
    """
    animals = AnimalSerializer(read_only=True, many=True)

    class Meta:
        model = Herd
        fields = ('pid', 'animals')


class DatetimeSerializer(serializers.Serializer):
    """
    Simple serializer to validate datetime
    """
    datetime = serializers.DateTimeField(required=True)
