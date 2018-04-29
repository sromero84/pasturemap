from datetime import datetime

from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from animals.models import Animal


class AnimalAPITestCase(TestCase):
    """
    Test the Animal API.
    """
    model = Animal

    def setUp(self):
        self.client = APIClient()

    def test_add_weight(self):
        animal = Animal.objects.create(pid=101)

        detail_url = reverse('animal-detail', kwargs={'pid': animal.pid})
        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['weight_entries']), 0)

        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal.pid})
        data = {'weight': 240.22, 'weigh_datetime': datetime.now()}
        response = self.client.post(add_weight_url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['weight_entries']), 1)
        self.assertEqual(response.data['weight_entries'][0]['weight'], '240.22')

    def test_total_weight(self):
        pass
