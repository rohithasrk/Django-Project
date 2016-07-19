from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime as dt
from django.contrib.auth.models import User


class Question(models.Model):
	question_text=models.CharField(max_length=200)
	pub_date=models.DateTimeField('Date published')

	def __str__(self):
		return self.question_text
	def was_published_recently(self):
		now=timezone.now()
		return now-dt.timedelta(days=1)<=self.pub_date<=now
	was_published_recently.admin_order_field='pub_date'
	was_published_recently.boolean=True
	was_published_recently.short_description='Published recently?'
	
class Choice(models.Model):
	question=models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text=models.CharField(max_length=200)
	votes=models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images',blank=True)

	def __unicode__(self):
		return self.user.username

class Voter(models.Model):
	user=models.ForeignKey(User)
	question=models.ForeignKey(Question)
