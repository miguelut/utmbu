from django.contrib.auth.models import User
from django.test import TestCase
from mbu.models import Scout, Troop, Council


class HomePageTests(TestCase):
    def test_home_page_redirect_on_logged_out(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)


class EditProfileTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='Gracie', password='Gracie')
        self.set_up_troops_and_councils()
        self.logged_in = self.client.login(username='Gracie', password='Gracie')

    def set_up_troops_and_councils(self):
        council = Council(name='Gracie Academy')
        council.save()
        troop = Troop()
        troop.number = '123'
        troop.council = council
        troop.save()

    def test_edit_profile_success(self):
        expected_troop = Troop.objects.get(pk=1)
        expected_form = {
            'first_name': 'Helio',
            'last_name': 'Gracie',
            'email': 'gracie@gmail.com',
            'scout-0-dob': '1913-10-01',
            'scout-0-rank': 'RED BELT',
            'scout-0-troop': expected_troop.id,

            'scout-TOTAL_FORMS': '1',
            'scout-INITIAL_FORMS': '0',
            'scout-MIN_NUM_FORMS': '0',
            'scout-MAX_NUM_FORMS': '1'
        }
        response = self.client.post('/scout/editprofile/', expected_form)

        updated_user = User.objects.get(username='Gracie')
        updated_scout = Scout.objects.all()[0]
        self.assertEqual(200, response.status_code)
        self.assertEqual('Helio', updated_user.first_name)
        self.assertEqual('Gracie', updated_user.last_name)
        self.assertEqual('gracie@gmail.com', updated_user.email)
        self.assertEqual('1913-10-01', updated_scout.dob.strftime('%Y-%m-%d'))
        self.assertEqual('RED BELT', updated_scout.rank)
        self.assertEqual(expected_troop, updated_scout.troop)