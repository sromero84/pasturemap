from decimal import Decimal

from scipy import interpolate

from django.db import models


class Herd(models.Model):
    """
    A group of unique animals, herds are disjoint.
    """
    pid = models.PositiveIntegerField(unique=True)  # Pasture ID


class Animal(models.Model):
    """
    Representation of an animal.
    """
    pid = models.PositiveIntegerField(unique=True)  # Pasture ID
    herd = models.ForeignKey(
        'Herd', related_name='animals', null=True, blank=True, on_delete=models.SET_NULL)

    def calculate_weight(self, ask_datetime):
        """
        Calculate the interpolation or extrapolation of the animal weight for a given date and time.

        :param ask_datetime: the point in time where weight want to be calculated
        :type ask_datetime: datetime.datetime

        :return: the value of the estimated weight of the animal at the given `ask_datetime`
        :rtype: Decimal
        """
        weight_entries_count = self.weight_entries.all().count()
        if weight_entries_count == 0:
            return None

        times = []
        weights = []
        for entry in self.weight_entries.order_by('weigh_datetime'):
            times.append(entry.weigh_datetime.timestamp())  # use timestamp for interpolate
            weights.append(entry.weight)

        extrapolation = interpolate.interp1d(times, weights, fill_value='extrapolate')
        return Decimal(extrapolation(ask_datetime.timestamp()).item(0))

    def get_weight_entries(self):
        """Return all the weigh entries for the animal, in the default order"""
        return self.weight_entries.all()


class WeightEntry(models.Model):
    """
    A weigh done at point in time for a given animal.
    """
    animal = models.ForeignKey('Animal', related_name='weight_entries', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=8, decimal_places=2)  # in kilograms
    weigh_datetime = models.DateTimeField()

    class Meta:
        ordering = ['weigh_datetime']
