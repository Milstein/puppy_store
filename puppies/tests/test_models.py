from django.urls import reverse
from django.test import TestCase
from django.test import Client

from ..models import Puppy


class PuppyTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')

        # Every test needs a client.
        self.client = Client()

    def test_puppy_breed(self):
        puppy_casper = Puppy.objects.get(name='Casper')
        puppy_muffin = Puppy.objects.get(name='Muffin')
        self.assertEqual(
            puppy_casper.get_breed(), "Casper belongs to Bull Dog breed.")
        self.assertEqual(
            puppy_muffin.get_breed(), "Muffin belongs to Gradane breed.")
        self.assertEqual(puppy_muffin.__unicode__(), puppy_muffin.name)

    def create_puppy(self, name='Casper', age=3, breed='Bull Dog', color='Black'):
        return Puppy.objects.create(name=name, age=age, breed=breed, color=color)

    def test_puppy_creation(self):
        p = self.create_puppy()
        self.assertTrue(p.__repr__(), p.name + ' is added.')
        self.assertEqual(p.__unicode__(), p.name)

    def test_puppy_list_view(self):
        p = self.create_puppy()
        url = reverse('puppies:index')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(p, resp.context['puppy'])
        # print(resp.context['puppy'])
        self.assertIn(p.name, [o.name for o in resp.context['puppy'].filter(name='Casper')])
        self.assertTrue(resp.context['puppy'].filter(name=p.name).exists())
