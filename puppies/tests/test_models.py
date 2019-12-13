import os
from django.conf import settings
from django.urls import reverse
from django.test import TestCase
from django.test import Client
from rest_framework import status
from rest_framework.utils import json
from selenium import webdriver

from puppies.forms import PuppyForm
from puppies.serializers import PuppySerializer
from ..models import Puppy


class PuppyTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')

        self.rambo = Puppy.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')
        self.ricky = Puppy.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

        """ Test payload for inserting a new puppy """
        self.valid_payload = {
            'name': 'Muffin',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

        """ Test module for updating an existing puppy record """
        self.muffin = Puppy.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')
        self.valid_payload = {
            'name': 'Muffy',
            'age': 2,
            'breed': 'Labrador',
            'color': 'Black'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

        # Every test needs a client.
        self.client = Client()

        # selenium
        path = os.path.join(settings.MEDIA_ROOT, 'geckodriver.exe')
        self.driver = webdriver.Firefox(executable_path=path)
        # self.driver.get('http://inventwithpython.com')

    def test_puppy_breed(self):
        puppy_casper = Puppy.objects.get(name='Casper')
        puppy_muffin = Puppy.objects.get(name='Muffin')
        self.assertEqual(
            puppy_casper.get_breed(), "Casper belongs to Bull Dog breed.")
        self.assertEqual(
            puppy_muffin.get_breed(), "Muffin belongs to Gradane breed.")
        self.assertEqual(puppy_muffin.__unicode__(), puppy_muffin.name)

    # views (uses selenium)
    def test_add_puppy(self):
        self.driver.get("http://localhost:8000/add/")
        self.driver.find_element_by_id('id_name').send_keys("test name")
        self.driver.find_element_by_id('id_age').send_keys(1)
        self.driver.find_element_by_id('id_breed').send_keys("test breed")
        self.driver.find_element_by_id('id_color').send_keys("test color")
        self.driver.find_element_by_id('submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    # forms
    def test_valid_form(self):
        p = Puppy.objects.create(name='Casper', age=3, breed='Bull Dog', color='Black')
        data = {'name': p.name, 'age': p.age, 'breed': p.breed, 'color': p.color}
        form = PuppyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        p = Puppy.objects.create( name='Muffy', age=1, breed='Gradane', color='Brown')
        data = {'name': p.name, 'age': p.age, 'breed': p.breed, 'color': p.color}
        form = PuppyForm(data=data)
        self.assertFalse(form.is_valid())

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

    # Test module for GET all puppies API
    def test_get_all_puppies(self):
        # get API response
        response = self.client.get(reverse('puppies:get_post_puppies'))
        # get data from db
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test module for GET single puppy API
    def test_get_valid_single_puppy(self):
        response = self.client.get(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
        puppy = Puppy.objects.get(pk=self.rambo.pk)
        # puppy = Puppy.objects.get(pk=self.ricky.pk)
        serializer = PuppySerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = self.client.get(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test module for inserting a new puppy
    def test_create_valid_puppy(self):
        response = self.client.post(
            reverse('puppies:get_post_puppies'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_puppy(self):
        response = self.client.post(
            reverse('puppies:get_post_puppies'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test module for updating an existing puppy record
    def test_valid_update_puppy(self):
        response = self.client.put(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_puppy(self):
        response = self.client.put(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test module for deleting an existing puppy record
    def test_valid_delete_puppy(self):
        response = self.client.delete(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = self.client.delete(
            reverse('puppies:get_delete_update_puppy', kwargs={'pk': 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        self.driver.quit
