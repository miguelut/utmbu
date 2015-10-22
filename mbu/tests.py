from django.contrib.auth.models import User
from django.test import TestCase
from mbu.models import Troop, Scout, Scoutmaster, CourseInstance, TimeBlock, MeritBadgeUniversity
from mbu.forms import ScoutProfileForm, ScoutmasterProfileForm
from mbu.course_utils import do_sessions_overlap, has_overlapping_enrollment
from mbu.views import _create_scout_enrollment_dict


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

    def test_should_not_register_user_as_scout_if_already_a_scoutmaster(self):
        Scoutmaster(user=self.user).save()

        response = self.client.get('/register/scout/')
        self.assertRedirects(response, '/')

        self.assertEqual(0, Scout.objects.filter(user=self.user).count())

    def test_should_not_register_user_as_scoutmaster_if_already_a_scout(self):
        Scout(user=self.user).save()

        response = self.client.get('/register/scoutmaster/')

        self.assertEqual(0, Scoutmaster.objects.filter(user=self.user).count())
        self.assertRedirects(response, '/')


class CourseEnrollmentTests(TestCase):
    fixtures = ['test_users', 'test_courses_courseinstances']

    def setUp(self):
        self.client.login(username='Gracie', password='Gracie')
        self.user = User.objects.get(username='Gracie')

    def should_enroll_in_course(self):
        request = {'course_instance_id': '1'}

        response = self.client.post('/scout/enroll_course/', request)

        self.assertEqual(200, response.status_code)
        self.assertEqual('{"result": true}', response.content)

    def should_not_enroll_in_course_if_overlapping_session(self):
        course_instance = CourseInstance.objects.get(pk=1)
        self.user.enrollments.add(course_instance)
        self.user.save()
        request = {'course_instance_id': '2'}

        response = self.client.post('/scout/enroll_course/', request)

        self.assertEqual(200, response.status_code)
        self.assertEqual('{"result": false}', response.content)


class HelperMethods(TestCase):
    fixtures = ['test_users',
                'test_courses_courseinstances',
                'test_scouts',
                'test_troops_councils'
               ]

    def should_create_scout_class_dict(self):
        scouts = Scout.objects.all()

        result = _create_scout_enrollment_dict(scouts)
        first_enrollment = result[scouts[0]][0]
        second_enrollment = result[scouts[0]][1]
        number_of_enrollments = len(result[scouts[0]])

        self.assertEqual(2, number_of_enrollments)
        self.assertEqual(CourseInstance.objects.get(pk=1), first_enrollment)
        self.assertEqual(CourseInstance.objects.get(pk=2), second_enrollment)


class CourseUtilsTest(TestCase):
    fixtures = ['test_users', 'test_courses_courseinstances']

    def setUp(self):
        self.client.login(username='Gracie', password='Gracie')
        self.user = User.objects.get(username='Gracie')

    def sessions_should_overlap_if_they_have_same_start_end_times(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)
        session2 = TimeBlock.objects.create(name='session2', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)

        result = do_sessions_overlap(session1, session2)

        self.assertTrue(result)

    def sessions_should_overlap_if_one_session_occurs_within_another_starting_at_same_time(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)
        overlapping_session = TimeBlock.objects.create(name='session2', start_time='2015-01-01 00:00:00', end_time='2015-01-01 00:30:00', mbu=mbu)

        result = do_sessions_overlap(session1, overlapping_session)

        self.assertTrue(result)

    def sessions_should_overlap_if_one_session_occurs_within_another_ending_at_same_time(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)
        overlapping_session = TimeBlock.objects.create(name='session2', start_time='2015-01-01 00:30:00', end_time='2015-01-01 01:00:00', mbu=mbu)

        result = do_sessions_overlap(session1, overlapping_session)

        self.assertTrue(result)

    def sessions_should_overlap_if_one_session_occurs_within_another(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)
        overlapping_session = TimeBlock.objects.create(name='session2', start_time='2015-01-01 00:30:00', end_time='2015-01-01 00:35:00', mbu=mbu)

        result = do_sessions_overlap(session1, overlapping_session)

        self.assertTrue(result)

    def sessions_should_not_overlap_if_one_session_occurs_before_another(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 00:00:00', end_time='2015-01-01 01:00:00', mbu=mbu)
        overlapping_session = TimeBlock.objects.create(name='session2', start_time='2015-01-01 01:00:00', end_time='2015-01-01 02:00:00', mbu=mbu)

        result = do_sessions_overlap(session1, overlapping_session)

        self.assertFalse(result)

    def sessions_should_not_overlap_if_one_session_occurs_after_another(self):
        mbu = MeritBadgeUniversity.objects.get(pk=1)
        session1 = TimeBlock.objects.create(name='session1', start_time='2015-01-01 02:00:00', end_time='2015-01-01 03:00:00', mbu=mbu)
        overlapping_session = TimeBlock.objects.create(name='session2', start_time='2015-01-01 01:00:00', end_time='2015-01-01 02:00:00', mbu=mbu)

        result = do_sessions_overlap(session1, overlapping_session)

        self.assertFalse(result)

    def should_return_true_if_enrolling_in_overlapping_course(self):
        course_instance = CourseInstance.objects.get(pk=1)
        self.user.enrollments.add(course_instance)
        self.user.save()
        overlapping_course_to_enroll = CourseInstance.objects.get(pk=2)

        result = has_overlapping_enrollment(self.user, overlapping_course_to_enroll)

        self.assertTrue(result)

    def should_return_false_if_enrolling_in_course_with_no_overlaps(self):
        overlapping_course_to_enroll = CourseInstance.objects.get(pk=2)

        result = has_overlapping_enrollment(self.user, overlapping_course_to_enroll)

        self.assertFalse(result)