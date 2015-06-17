from django.contrib.auth.models import User
from django.test import TestCase
from mbu.models import Troop, Council
from mbu.forms import ScoutProfileForm


class HomePageTests(TestCase):
    def test_home_page_redirect_on_logged_out(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)


class EditProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Gracie', password='Gracie')
        self.set_up_troops_and_councils()
        self.logged_in = self.client.login(username='Gracie', password='Gracie')

    def set_up_troops_and_councils(self):
        council = Council(name='Gracie Academy')
        council.save()
        troop = Troop()
        troop.number = '123'
        troop.council = council
        troop.save()

    def test_edit_scout_profile_success(self):
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'email': 'gracie@gmail.com',
            'dob': '1913-10-01',
            'rank': 'RED BELT',
            'troop': expected_troop.id
        }
        response = self.client.post('/scout/profile/edit/', expected_form)

        updated_user = User.objects.get(username='Gracie')
        updated_scout = updated_user.scout
        self.assertEqual(200, response.status_code)
        self.assertEqual('Helio', updated_user.first_name)
        self.assertEqual('Gracie', updated_user.last_name)
        self.assertEqual('gracie@gmail.com', updated_user.email)
        self.assertEqual('1913-10-01', updated_scout.dob.strftime('%Y-%m-%d'))
        self.assertEqual('RED BELT', updated_scout.rank)
        self.assertEqual(expected_troop, updated_scout.troop)

    def test_scout_form_should_not_be_valid(self):
        expected_form = {}
        scout_form = ScoutProfileForm(expected_form, instance=self.user)

        self.assertFalse(scout_form.is_valid())

    def test_scout_form_should_be_valid(self):
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'dob': '2014-01-01',
            'rank': 'RED BELT',
            'troop': expected_troop.pk
        }
        scout_form = ScoutProfileForm(expected_form, instance=self.user)

        self.assertTrue(scout_form.is_valid())