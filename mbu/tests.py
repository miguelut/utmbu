from django.test import TestCase

class HomePageTests(TestCase):
	def test_home_page_redirect_on_logged_out(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)
