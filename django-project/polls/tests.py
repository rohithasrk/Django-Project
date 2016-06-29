import datetime as dt
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Question
# Create your tests here.

def create_question(question_text, days):
	""" Creates a question with the given question_text and published the given numbers of `days` offset to now"""
	time = timezone.now()+dt.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)
	
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

class QuestionViewTests(TestCase):
	
	def test_index_view_with_no_questions(self):
		"""If no questions exist, an appropriate message should be displayed"""
		response=self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_a_past_question(self):
		"""Questions with a pub_date in the past should be displayed on the index page"""
		create_question(question_text="Past Question",days=-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past Question>'])
	
	def test_index_view_with_a_future_question(self):
		"""Questions with a future pub_date shouldn't be displayed in the index page"""
		create_question(question_text="Future question",days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertContains(response,"No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	
	def test_index_view_with_future_question_and_past_question(self):
		""" Even if both past and future questions exist, only past ones shall be displayed."""
		create_question(question_text="Past Question", days=-30)
		create_question(question_text="Future Question",days=30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past Question>'])
	def test_index_view_with_two_past_questions(self):
		"""It should display both the questions"""
		create_question(question_text="Past 1",days=-5)
		create_question(question_text="Past 2",days=-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past 1>','<Question: Past 2>'])

class QuestionIndexDetailView(TestCase):
	
	def test_detail_view_with_a_future_question(self):
		""" The detail view of a question with a pub_date in the future should return 404 not found. """
		future_question=create_question(question_text="Future question",days=5)
		url=reverse('polls:detail',args=(future_question.id,))
		response=self.client.get(url)
		self.assertEqual(response.status_code,404)
		
	def test_detail_view_with_a_past_question(self):
		"""The detail view of a question with a pub_date in the past should be displayed in the question's text"""
		past_question=create_question(question_text="Past question",days=-5)
		url=reverse('polls:detail',args=(past_question.id,))
		response=self.client.get(url)
		self.assertContains(response,past_question.question_text)
		
