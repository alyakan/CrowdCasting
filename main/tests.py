from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from main.models import Actor, Experience


class ExperienceTestCase(APITestCase):

    def test_actor_add_experience(self):
        user = User.objects.create_user(username="johndoe", password="1234")
        user.save()
        self.client = APIClient()
        self.client.login(username='johndoe', password='1234')
        actor = Actor.objects.create(user_id=user.id)
        init_exp_count = Experience.objects.count()
        url = reverse('experience-list')
        data = {'experience': 'movie', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(Experience.objects.count(), init_exp_count + 1)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.get(actor_id=actor.id))

    def test_experience_field_required(self):
        user = User.objects.create_user(username="johndoe", password="1234")
        user.save()
        self.client = APIClient()
        self.client.login(username='johndoe', password='1234')
        Actor.objects.create(user_id=user.id)
        init_exp_count = Experience.objects.count()
        url = reverse('experience-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(Experience.objects.count(), init_exp_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_experience(self):
        user = User.objects.create_user(username="johndoe", password="1234")
        user.save()
        self.client = APIClient()
        self.client.login(username='johndoe', password='1234')
        Actor.objects.create(user_id=user.id)
        url = reverse('experience-list')
        data = {'experience': 'movie', }
        self.client.post(url, data, format='json')
        url = reverse('experience-detail', kwargs={'pk': 1})
        data = {'experience': 'movie-update'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Experience.objects.get(id=1).experience, 'movie-update')

    def test_delete_experience(self):
        user = User.objects.create_user(username="johndoe", password="1234")
        user.save()
        self.client = APIClient()
        self.client.login(username='johndoe', password='1234')
        Actor.objects.create(user_id=user.id)
        url = reverse('experience-list')
        data = {'experience': 'movie', }
        self.client.post(url, data, format='json')
        exp_count = Experience.objects.count()
        url = reverse('experience-detail', kwargs={'pk': 1})
        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Experience.objects.count(), exp_count - 1)


class RequestAccountTestCase(APITestCase):
    