##########################
# SnippetManager model
##########################

from django.db import models
from django.contrib.auth.models import User
import editarea
from django.db.models import Q
# Create your models here.
class CodeManager(models.Manager):
	def getShortSnippets(self, user):
		snippets = Code.objects.filter(
			Q(user=user),
			Q(delete_date=None)
		).order_by('-create_date')[:200]

		return_snippet = []
		for snippet in snippets:
			code = snippet.code
			s_code = code[:500] + '...'
			desc = snippet.description
			s_desc = desc[:100] + '...'

			new_snippet = {
				'id': snippet.id,
				'code': s_code,
				'description': s_desc,
				'title': snippet.title,
				'category_name': snippet.category.name,
				'public': snippet.public,
				'improve': snippet.improvement
			}
			return_snippet.append(new_snippet)

		return return_snippet

	def getShortSnippetsSorted(self, project, cat, project_id, cat_id, user, keyword):
		snippets_list = {}

		if project_id == 0 and cat_id != 0:
			snippets_list = Code.objects.filter(
				Q(user=user),
				Q(category=cat),
				Q(delete_date=None),
				Q(title__icontains=keyword) | Q(description__icontains=keyword)
			).order_by('-create_date')[:200]

		if cat_id == 0 and project_id != 0:
			snippets_list = Code.objects.filter(
				Q(user=user),
				Q(project=project),
				Q(delete_date=None),
				Q(title__icontains=keyword) | Q(description__icontains=keyword)
			).order_by('-create_date')[:200]

		if project_id != 0 and cat_id != 0:
			snippets_list = Code.objects.filter(
				Q(user=user),
				Q(category=cat),
				Q(project=project),
				Q(delete_date=None),
				Q(title__icontains=keyword) | Q(description__icontains=keyword)
			).order_by('-create_date')[:200]

		if project_id == 0 and cat_id == 0:
			snippets_list = Code.objects.filter(
				Q(user=user),
				Q(delete_date=None),
				Q(title__icontains=keyword) | Q(description__icontains=keyword)
			).order_by('-create_date')[:200]

		return_snippet = []
		for snippet in snippets_list:
			code = snippet.code
			s_snippet = code[:500] + '...'
			desc = snippet.description
			s_desc = desc[:100] + '...'

			new_snippet = {
				'id': snippet.id,
				'title': snippet.title,
				'description': s_desc,
				'category_name': snippet.category.name,
				'code': s_snippet,
				'public': snippet.public,
				'improve': snippet.improvement
			}
			
			return_snippet.append(new_snippet)

		return return_snippet

	def getWorldShortSnippetsSorted(self, cat, cat_id, keyword):
		snippets_list = {}

		if cat_id != 0:
			snippets_list = Code.objects.filter(
				Q(category=cat),
				Q(title__icontains=keyword) | Q(description__icontains=keyword),
				Q(delete_date=None)
			).order_by('-create_date')
		else:
			snippets_list = Code.objects.filter(
				Q(title__icontains=keyword) | Q(description__icontains=keyword),
				Q(delete_date=None)
			).order_by('-create_date')

		return_snippet = []
		for snippet in snippets_list:
			code = snippet.code
			s_snippet = code[:500] + '...'
			desc = snippet.description
			s_desc = desc[:100] + '...'

			new_snippet = {
				'id': snippet.id,
				'title': snippet.title,
				'description': s_desc,
				'category_name': snippet.category.name,
				'code': s_snippet,
				'public': snippet.public,
				'improve': snippet.improvement
			}
			
			return_snippet.append(new_snippet)

		return return_snippet

class Category(models.Model):
	name = models.CharField(max_length=25, unique=True)
	create_date = models.DateTimeField()
	delete_date = models.DateTimeField(null=True)
	user = models.ForeignKey(User)

class Project(models.Model):
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User)

class Code(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=500)
	code = editarea.EditAreaField()
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	category = models.ForeignKey(Category)
	public = models.BooleanField()
	improvement = models.BooleanField()
	create_date = models.DateTimeField()
	update_date = models.DateTimeField()
	delete_date = models.DateTimeField(null=True)
	objects = CodeManager()

class Vote(models.Model):
	date = models.DateTimeField()
	score = models.PositiveSmallIntegerField()
	user = models.ForeignKey(User)
	code = models.ForeignKey(Code)
	
class Rating(models.Model):
	user = models.ForeignKey(User)
	score = models.PositiveIntegerField()
	update_date = models.DateTimeField()

class Points(models.Model):
	points = models.PositiveIntegerField()
	user = models.ForeignKey(User)

class Viewlog(models.Model):
	view_date = models.DateTimeField()
	user = models.ForeignKey(User)
	code = models.ForeignKey(Code)

class DisqusComment(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField()
	disqus_id = models.PositiveIntegerField()
	comment = models.TextField()
	code = models.ForeignKey(Code)

class SnippetImprovement(models.Model):
	user = models.ForeignKey(User)
	code = models.ForeignKey(Code)
	submit_date = models.DateTimeField()
	new_code = editarea.EditAreaField()
	approve_date = models.DateTimeField(null=True)
	disapprove_date = models.DateTimeField(null=True)

class FacebookLogin(models.Model):
	facebook_id = models.PositiveIntegerField()
	user = models.ForeignKey(User)

class GoogleLogin(models.Model):
	google_id = models.CharField(max_length=30)
	user = models.ForeignKey(User)
