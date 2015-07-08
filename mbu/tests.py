from django.contrib.auth.models import User
from django.test import TestCase
from mbu.models import Troop, Scout, Scoutmaster
from mbu.forms import ScoutProfileForm, ScoutmasterProfileForm


class EditScoutProfileTests(TestCase):
    fixtures = ['test_users', 'test_troops_councils']

    def setUp(self):
        self.client.login(username='Gracie', password='Gracie')
        self.user = User.objects.get(username='Gracie')

    def test_edit_scout_profile_success(self):
        Scout(user=self.user).save()
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'email': 'gracie@gmail.com',
            'troop': expected_troop.id
        }

        response = self.client.post('/scout/profile/edit/', expected_form)

        updated_user = User.objects.get(username='Gracie')
        updated_scout = updated_user.scout
        self.assertEqual(200, response.status_code)
        self.assertEqual('Helio', updated_user.first_name)
        self.assertEqual('Gracie', updated_user.last_name)
        self.assertEqual('gracie@gmail.com', updated_user.email)
        self.assertEqual(expected_troop, updated_scout.troop)

    def test_edit_scout_profile_form_should_prepopulate_fields(self):
        Scout(user=self.user).save()
        # Given a profile
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'troop': expected_troop.id
        }
        self.client.post('/scout/profile/edit/', expected_form)

        response = self.client.get('/scout/profile/edit/')

        self.assertEqual(response.context['form'].initial['first_name'], "Helio")
        self.assertEqual(response.context['form'].initial['last_name'], "Gracie")
        self.assertEqual(response.context['form'].initial['email'], "")
        self.assertEqual(response.context['profile_form'].initial['troop'], 1)

    def test_redirect_if_not_scout(self):
        response = self.client.get('/scout/profile/edit/')

        self.assertRedirects(response, 'login/?next=/scout/profile/edit/')

    def test_should_not_redirect_from_edit_profile_page_if_scout(self):
        Scout(user=self.user).save()

        response = self.client.get('/scout/profile/edit/')

        self.assertEqual(200, response.status_code)

    def test_scout_form_should_be_valid(self):
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'troop': expected_troop.pk
        }
        scout_form = ScoutProfileForm(expected_form)

        self.assertTrue(scout_form.is_valid())


class EditScoutmasterProfileTests(TestCase):
    fixtures = ['test_users', 'test_troops_councils']

    def setUp(self):
        self.client.login(username='Gracie', password='Gracie')
        self.user = User.objects.get(username='Gracie')

    def test_edit_scoutmaster_profile_success(self):
        Scoutmaster(user=self.user).save()
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'email': 'gracie@gmail.com',
            'troop': expected_troop.id
        }

        response = self.client.post('/scoutmaster/profile/edit/', expected_form)

        updated_user = User.objects.get(username='Gracie')
        updated_scoutmaster = updated_user.scoutmaster
        self.assertEqual(200, response.status_code)
        self.assertEqual('Helio', updated_user.first_name)
        self.assertEqual('Gracie', updated_user.last_name)
        self.assertEqual('gracie@gmail.com', updated_user.email)
        self.assertEqual(expected_troop, updated_scoutmaster.troop)

    def test_edit_scoutmaster_profile_form_should_prepopulate_fields(self):
        Scoutmaster(user=self.user).save()
        # Given a profile
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'troop': expected_troop.id
        }
        self.client.post('/scoutmaster/profile/edit/', expected_form)

        response = self.client.get('/scoutmaster/profile/edit/')

        self.assertEqual(response.context['form'].initial['first_name'], "Helio")
        self.assertEqual(response.context['form'].initial['last_name'], "Gracie")
        self.assertEqual(response.context['form'].initial['email'], "")
        self.assertEqual(response.context['profile_form'].initial['troop'], 1)

    def test_redirect_if_not_scoutmaster(self):
        response = self.client.get('/scoutmaster/profile/edit/')

        self.assertRedirects(response, 'login/?next=/scoutmaster/profile/edit/')

    def test_should_not_redirect_from_edit_profile_page_if_scoutmaster(self):
        Scoutmaster(user=self.user).save()

        response = self.client.get('/scoutmaster/profile/edit/')

        self.assertEqual(200, response.status_code)

    def test_scoutmaster_form_should_be_valid(self):
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'troop': expected_troop.pk
        }
        scoutmaster_form = ScoutmasterProfileForm(expected_form)

        self.assertTrue(scoutmaster_form.is_valid())


class RegisterUserTypeTests(TestCase):
    fixtures = ['test_users', 'test_troops_councils']

    def setUp(self):
        self.client.login(username='Gracie', password='Gracie')
        self.user = User.objects.get(username='Gracie')

    def test_should_register_user_as_scout_if_not_already_a_scoutmaster(self):
        response = self.client.get('/register/scout/')

        self.assertIsNotNone(Scout.objects.get(user=self.user))
        self.assertRedirects(response, 'scout/profile/edit/')

    def test_should_not_register_user_as_scout_if_already_a_scoutmaster(self):
        Scoutmaster(user=self.user).save()

        response = self.client.get('/register/scout/')
        self.assertRedirects(response, '/')

        self.assertEqual(0, Scout.objects.filter(user=self.user).count())

    def test_should_register_user_as_scoutmaster_if_not_already_a_scout(self):
        response = self.client.get('/register/scoutmaster/')

        self.assertIsNotNone(Scoutmaster.objects.get(user=self.user))
        self.assertRedirects(response, 'scoutmaster/profile/edit/')

    def test_should_not_register_user_as_scoutmaster_if_already_a_scout(self):
        Scout(user=self.user).save()

        response = self.client.get('/register/scoutmaster/')

        self.assertEqual(0, Scoutmaster.objects.filter(user=self.user).count())
        self.assertRedirects(response, '/')