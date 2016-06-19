import datetime as dt
from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.

class QuestionMethodTests(TestCase):
	
	def test_was_published_recently_with_future_question(self):
		"""was_published_recently() should return False for questions whose pub_date is in the future."""
		time=timezone.now() + dt.timedelta(days=30)
		future_question=Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)
	
	def test_was_published_recently_with_old_question(self):
		"""was_pubished_recently() should return False for questions which are older than one day."""
		time=timezone.now()-dt.timedelta(days=30)
		old_question=Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)
	
	def test_was_published_recently_with_recent_question(self):
		"""was_published_recently() should return True for question published within one day."""
		time=timezone.now()-dt.timedelta(hours=1)
		recent_question=Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)
