from __future__ import unicode_literals
from django.db import models

#@python_2_unicode_compatible
class Question(models.Model):
	question_text=models.CharField(max_length=200)
	pub_date=models.DateTimeField('Date published')

	def __str__(self):
		return self.question_text
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	
#@python_2_unicode_compatible
class Choice(models.Model):
	question=models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text=models.CharField(max_length=200)
	votes=models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text
