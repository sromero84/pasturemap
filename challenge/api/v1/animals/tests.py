from datetime import datetime

from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from animals.models import Animal, Herd


class AnimalAPITestCase(TestCase):
    """
    Test the Animal API.
    """

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        """Remove all animals before each test case"""
        Animal.objects.all().delete()

    def test_add_weight(self):
        """
        Test add a weigh for an animal.
        """
        animal = Animal.objects.create(pid=101)

        detail_url = reverse('animal-detail', kwargs={'pid': animal.pid})
        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['weight_entries']), 0)

        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal.pid})
        data = {'weight': 240.22, 'weigh_datetime': datetime.now()}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['weight_entries']), 1)
        self.assertEqual(response.data['weight_entries'][0]['weight'], '240.22')

    def test_add_weight_error(self):
        """
        Test add a weigh for an animal with incorrect value
        """
        animal = Animal.objects.create(pid=101)

        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal.pid})
        data = {'weight': 'bad_value', 'weigh_datetime': datetime.now()}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_total_weight(self):
        animal_1 = Animal.objects.create(pid=101)
        animal_2 = Animal.objects.create(pid=102)

        # add weightings for animal 1: 100 (day 1) and 200 (day 21) -> steps of 5
        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal_1.pid})
        data = {'weight': 100, 'weigh_datetime': '2018-04-01T10:00:00Z'}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 200)

        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal_1.pid})
        data = {'weight': 200, 'weigh_datetime': '2018-04-21T10:00:00Z'}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 200)

        # add weightings for animal 2: 200 (day 1) and 300 (day 11) -> steps of 10
        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal_2.pid})
        data = {'weight': 200, 'weigh_datetime': '2018-04-01T10:00:00Z'}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 200)

        add_weight_url = reverse('animal-add-weight', kwargs={'pid': animal_2.pid})
        data = {'weight': 300, 'weigh_datetime': '2018-04-11T10:00:00Z'}
        response = self.client.post(add_weight_url, data=data)
        self.assertEqual(response.status_code, 200)

        total_weight_url = reverse('animal-total-weight')
        data = {'datetime': '2018-04-11T10:00:00Z'}  # request at day 11: 150 + 300 / 2
        response = self.client.post(total_weight_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_weight'], 225.00)

    def test_total_weight_error(self):
        """Test total weight endpoint sending invalid data"""
        total_weight_url = reverse('animal-total-weight')
        data = {'datetime': 66.9}
        response = self.client.post(total_weight_url, data=data)
        self.assertEqual(response.status_code, 400)


class HerdAPITestCase(TestCase):
    """
    Test the Herd API.
    """
    def setUp(self):
        self.client = APIClient()

    def test_add_animal(self):
        """Test add animal to given Herd"""
        animal_1 = Animal.objects.create(pid=101)
        animal_2 = Animal.objects.create(pid=102)

        herd = Herd.objects.create(pid=303)
        herd.animals.add(animal_1)

        detail_url = reverse('herd-detail', kwargs={'pid': herd.pid})
        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['animals']), 1)

        add_animal_url = reverse('herd-add-animal', kwargs={'pid': herd.pid})
        data = {'animal_pid': animal_2.pid}
        response = self.client.post(add_animal_url, data=data)
        self.assertEqual(response.status_code, 200)

        detail_url = reverse('herd-detail', kwargs={'pid': herd.pid})
        response = self.client.get(detail_url)
        self.assertEqual(len(response.data['animals']), 2)

    def test_add_animal_error(self):
        """Test add animal to Herd with incorrect values"""
        herd = Herd.objects.create(pid=303)

        add_animal_url = reverse('herd-add-animal', kwargs={'pid': herd.pid})
        data = {'animal_pid': 777}
        response = self.client.post(add_animal_url, data=data)
        self.assertEqual(response.status_code, 404)

        add_animal_url = reverse('herd-add-animal', kwargs={'pid': 999})
        response = self.client.post(add_animal_url, data=data)
        self.assertEqual(response.status_code, 404)
