##################################
# SnippetManager Views Controller
##################################

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.utils import simplejson, timezone
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from snippetmanager.models import Category, Code, Project, Viewlog, DisqusComment, SnippetImprovement, FacebookLogin, GoogleLogin
from django.contrib.auth.models import User
import difflib

# New Snippet Form Validation
class NewSnippetForm(forms.Form):
	title = forms.CharField(max_length=50)
	description = forms.CharField(max_length=500)
	snippet = forms.CharField()
	snippet_type = forms.IntegerField()
	project = forms.IntegerField()

# SourceWorld Page
def snippet_world(request):
	notify_count = 0
	notification = {}
	if request.user.is_authenticated:
		get_notify = get_notify_count(request.user.id)
		notify_count = get_notify['count']
		notification = get_notify['data']

	cats = Category.objects.all()
	snippets_list = Code.objects.filter(public=1, delete_date=None).order_by('-create_date')[:200]

	short_snippets_list = []
	for snippet in snippets_list:
		code = snippet.code
		s_code = code[:500] + '...'

		desc = snippet.description
		s_desc = desc[:100] + '...'

		short_snippets_list.append({
			'id': snippet.id,
			'title': snippet.title,
			'description': s_desc,
			'code': s_code,
			'category_name': snippet.category.name,
			'improve': snippet.improvement
		})

	paginator = Paginator(short_snippets_list, 12)

	page = request.GET.get('page')

	try:
		snippets = paginator.page(page)
	except PageNotAnInteger:
		snippets = paginator.page(1)
	except EmptyPage:
		snippets = paginator.page(paginator.num_pages)

	context = {
		'page': 'snippetworld',
		'cats': cats,
		'snippets': snippets,
		'notify_count': notify_count,
		'notification': notification
	}

	return render(request, 'snippetmanager/snippet_world.html', context)

# SourceWorld Sorted
def snippet_world_sorted(request):
	if request.method == 'POST':
		notify_count = 0
		notification = {}
		if request.user.is_authenticated:
			get_notify = get_notify_count(request.user.id)
			notify_count = get_notify['count']
			notification = get_notify['data']

		cat_id = int(request.POST['category'])
		keyword = request.POST['keyword']

		cat = {}
		project = {}

		if cat_id != 0:
			cat = Category.objects.get(pk=cat_id)
		
		snippets_list = Code.objects.getWorldShortSnippetsSorted(cat, cat_id, keyword)

		cats = Category.objects.all()

		paginator = Paginator(snippets_list, 12)
		page = request.GET.get('page')

		try:
			snippets = paginator.page(page)
		except PageNotAnInteger:
			snippets = paginator.page(1)
		except EmptyPage:
			snippets = paginator.page(paginator.num_pages)

		context = {
			'page': 'snippetworld',
			'cats': cats,
			'snippets': snippets,
			'cat_id': cat_id,
			'notify_count': notify_count,
			'notification': notification
		}

		return render(request, 'snippetmanager/snippet_world.html', context)
	else:
		data = {
			'status': False,
			'message': 'permission_denied'
		}
		return HttpResponse(simplejson.dumps(data), 'application/json')		

# MySource Page
@login_required
def my_snippets(request):
	get_notify = get_notify_count(request.user.id)

	notify_count = get_notify['count']
	notification = get_notify['data']

	snippet_list = Code.objects.getShortSnippets(request.user)
	paginator = Paginator(snippet_list, 12)

	page = request.GET.get('page')

	try:
		snippets = paginator.page(page)
	except PageNotAnInteger:
		snippets = paginator.page(1)
	except EmptyPage:
		snippets = paginator.page(paginator.num_pages)

	cats = Category.objects.all()
	projects = Project.objects.filter(
		Q(pk=1) | Q(user=request.user)
	)

	context = {
		'page': 'mysnippets',
		'snippets': snippets,
		'cats': cats,
		'projects': projects,
		'notify_count': notify_count,
		'notification': notification
	}

	return render(request, 'snippetmanager/my_snippets.html', context)

# MySnippets Sort By Type
@login_required
def my_snippets_sorted(request):
	if request.method == 'POST':
		get_notify = get_notify_count(request.user.id)
		notify_count = get_notify['count']
		notification = get_notify['data']

		project_id = int(request.POST['project'])
		cat_id = int(request.POST['category'])
		keyword = request.POST['keyword']
		cat = {}
		project = {}

		if cat_id != 0:
			cat = Category.objects.get(pk=cat_id)
		
		if project_id != 0:
			project = Project.objects.get(pk=project_id)
		
		snippets_list = Code.objects.getShortSnippetsSorted(project, cat, project_id, cat_id, request.user, keyword)

		cats = Category.objects.all()
		projects = Project.objects.filter(
			Q(pk=1) | Q(user=request.user)
		)

		paginator = Paginator(snippets_list, 12)
		page = request.GET.get('page')

		try:
			snippets = paginator.page(page)
		except PageNotAnInteger:
			snippets = paginator.page(1)
		except EmptyPage:
			snippets = paginator.page(paginator.num_pages)

		context = {
			'page': 'mysnippets',
			'snippets': snippets,
			'cats': cats,
			'projects': projects,
			'cat_id': cat_id,
			'project_id': project_id,
			'notify_count': notify_count,
			'notification': notification
		}

		return render(request, 'snippetmanager/my_snippets.html', context)
	else:
		data = {
			'status': False,
			'message': 'permission_denied'
		}
		return HttpResponse(simplejson.dumps(data), 'application/json')

# Write new Snippet Page
@login_required
def new_snippet(request):
	get_notify = get_notify_count(request.user.id)
	notify_count = get_notify['count']
	notification = get_notify['data']
	
	# Getting categories
	cats = Category.objects.all()
	projects = Project.objects.filter(
		Q(pk=1) | Q(user=request.user)
	)

	context = {
		'page': 'new_snippet',
		'cats': cats,
		'projects': projects,
		'notify_count': notify_count,
		'notification': notification
	}

	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		cat_id = int(request.POST['snippet_type'])
		snippet = request.POST['snippet']
		project_id = int(request.POST['project'])
		public = False
		improve = False

		try:
			public = request.POST['public']
			public = True
		except:
			public = False

		try:
			improve = request.POST['improve']
			improve = True
		except:
			improve = False

		form = NewSnippetForm(request.POST); # Bound the form

		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			snippet_type = form.cleaned_data['snippet_type']
			snippet = form.cleaned_data['snippet']
			project_id = form.cleaned_data['project']

			new_snippet = Code(title=title, description=description, code=snippet, create_date=timezone.now(), update_date=timezone.now(), public=public, improvement=improve)

			category = Category.objects.get(pk=cat_id)
			project = Project.objects.get(pk=project_id)

			new_snippet.user = request.user
			new_snippet.category = category
			new_snippet.project = project

			new_snippet.save()

			return HttpResponseRedirect(reverse('snippetmanager:mysnippets'))
		else:
			posted_values = {
				'title': title,
				'cat_id': cat_id,
				'description': description,
				'snippet': snippet,
				'project_id': project_id,
				'public': public,
				'improve': improve
			}
			context.update(posted_values)
	else:
		form = NewSnippetForm()

	context['form'] = form

	return render(request, 'snippetmanager/new_snippet.html', context)

# Edit Snippets
@login_required
def edit_snippet(request, code_id):
	get_notify = get_notify_count(request.user.id)
	notify_count = get_notify['count']
	notification = get_notify['data']

	code = Code.objects.get(pk=code_id)
	cats = Category.objects.all()
	projects = Project.objects.filter(
		Q(pk=1) | Q(user=request.user)
	)

	context = {
		'page': 'edit_snippet',
		'code': code,
		'cats': cats,
		'projects': projects,
		'notify_count': notify_count,
		'notification': notification
	}

	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		cat_id = int(request.POST['snippet_type'])
		snippet = request.POST['snippet']
		project_id = int(request.POST['project'])

		public = False
		improve = False

		try:
			public = request.POST['public']
			public = True
		except:
			public = False

		try:
			improve = request.POST['improve']
			improve = True
		except:
			improve = False		

		form = NewSnippetForm(request.POST); # Bound the form

		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			snippet_type = form.cleaned_data['snippet_type']
			snippet = form.cleaned_data['snippet']

			#new_snippet = Code(title=title, description=description, code=snippet, create_date=timezone.now(), update_date=timezone.now())
			code.title = title
			code.description = description
			code.code = snippet
			code.update_date = timezone.now()
			code.public = public
			code.improvement = improve

			category = Category.objects.get(pk=cat_id)
			project = Project.objects.get(pk=project_id)

			code.user = request.user
			code.category = category
			code.project = project

			code.save()

			return HttpResponseRedirect(reverse('snippetmanager:edit_snippet', args=(code.id,)))
		else:
			posted_values = {
				'title': title,
				'cat_id': cat_id,
				'description': description,
				'snippet': snippet
			}
			context.update(posted_values)
	else:
		form = NewSnippetForm()

	context['form'] = form

	return render(request, 'snippetmanager/edit_snippet.html', context)

# Add New Project
@login_required
@csrf_exempt
def new_project(request):
	if request.method == 'POST':
		project_name = request.POST['project_name']
		user_id = request.POST['user_id']

		if len(project_name) <= 0:
			data = {
				'status': False,
				'error_code': 3,
				'message': 'empty_name'
			}
			return HttpResponse(simplejson.dumps(data), mimetype='application/json')

		user = User.objects.get(pk=user_id)
		# Check for duplicate project name
		try:
			check_duplicate_name = Project.objects.get(
				Q(name=project_name),
				Q(user=user)
			)
		except Project.DoesNotExist:
			new_project = Project(name=project_name)
			new_project.user = user
			new_project.save()

			data = {
				'status': True,
				'error_code': 0,
				'message': 'success'
			}
			return HttpResponse(simplejson.dumps(data), mimetype='application/json')

		data = {
			'status': False,
			'error_code': 2,
			'message': 'duplicate_name'
		}
		return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	else:
		data = {
			'status': False,
			'error_code': 1,
			'message': 'permission_denied'
		}
		return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Delete Snippet
@login_required
def delete_snippet(request, code_id):
	try:
		delete_snippet = Code.objects.get(pk=code_id)
		delete_snippet.delete_date = timezone.now()
		delete_snippet.save()
	except:
		return HttpResponseRedirect(reverse('snippetmanager:mysnippets'))

	return HttpResponseRedirect(reverse('snippetmanager:mysnippets'))

# View public snippet detail
@login_required
def public_snippet_detail(request, code_id):
	get_notify = get_notify_count(request.user.id)
	notify_count = get_notify['count']
	notification = get_notify['data']

	snippet = Code.objects.get(pk=code_id)
	cat = Category.objects.get(pk=snippet.category.id)

	context = {
		'page': 'public_snippet_detail',
		'snippet': snippet,
		'cat_name': cat.name,
		'notify_count': notify_count,
		'notification': notification
	}

	if request.method == 'POST':
		# check for duble submission
		try:
			snippet_improve = SnippetImprovement.objects.get(user=request.user, code=snippet, approve_date=None, disapprove_date=None)
			context.update({'error_code': 1})
		except SnippetImprovement.DoesNotExist:
			improved_snippet = request.POST['improved_snippet']

			new_snippet = SnippetImprovement(user=request.user, code=snippet, new_code=improved_snippet, submit_date=timezone.now())
			new_snippet.save()
			context.update({'error_code': 0})

	# check to see if the user has viewed this snippet already
	try:
		viewlog = Viewlog.objects.get(user=request.user, code=snippet)
	except Viewlog.DoesNotExist:
		viewlog = Viewlog(user=request.user, code=snippet, view_date=timezone.now())
		viewlog.save()

	return render(request, 'snippetmanager/public_snippet_detail.html', context)

# Record Disqus comments
@login_required
@csrf_exempt
def disqus_comment(request):
	if request.method == 'POST':
		try:
			user_id = request.POST['user_id']
			code_id = request.POST['code_id']
			disqus_id = request.POST['disqus_id']
			comment = request.POST['comment']
		except:
			context = {
				'status': False,
				'message': 'permission_denied'
			}
			return HttpResponse(simplejson.dumps(context), 'application/json')

		code = Code.objects.get(pk=code_id)
		user = User.objects.get(pk=user_id)

		comment = DisqusComment(user=user, date=timezone.now(), disqus_id=disqus_id, comment=comment, code=code)

		try:
			comment.save()
		except:
			context = {
				'status': False,
				'message': 'internal_error'
			}
			return HttpResponse(simplejson.dumps(context), 'application/json')

		context = {
			'status': True,
			'message': 'success'
		}
		return HttpResponse(simplejson.dumps(context), 'application/json')
	else:
		context = {
			'status': False,
			'message': 'permission_denied'
		}
		return HttpResponse(simplejson.dumps(context), 'application/json')

# New improved snippet notification
def get_notify_count(user_id):
	snippet_improve = SnippetImprovement.objects.filter(
		code__user__id=user_id,
		approve_date=None,
		disapprove_date=None
	)

	num_of_snippets = len(snippet_improve)

	context = {}

	if num_of_snippets > 0:
		context = {
			'count': num_of_snippets,
			'data': snippet_improve
		}
	else:
		context = {
			'count': 0,
			'data': {}
		}

	return context

# Show improved snippet comparison
@login_required
def improved_snippet_detail(request, improve_id):
	get_notify = get_notify_count(request.user.id)
	notify_count = get_notify['count']
	notification = get_notify['data']

	snippet_improve = SnippetImprovement.objects.get(pk=improve_id)

	snippet_after = snippet_improve.new_code
	snippet_before = snippet_improve.code.code

	snippet_after_text = snippet_after.splitlines()
	snippet_before_text = snippet_before.splitlines()

	d = difflib.Differ()

	diff = d.compare(snippet_before_text, snippet_after_text)
	
	context = {
		'page': 'improved_snippet_detail',
		'snippet_before': snippet_before,
		'snippet_after': '\n'.join(list(diff)),
		'cat_name': snippet_improve.code.category.name,
		'notify_count': notify_count,
		'notification': notification,
		'improve_id': improve_id,
		'first_name': snippet_improve.user.first_name,
		'submit_date': snippet_improve.submit_date,
		'title': snippet_improve.code.title
	}

	return render(request, 'snippetmanager/improved_snippet.html', context)

# Approve a updated snippet
@login_required
def approve_snippet(request, improve_id):
	try:
		improved_snippet = SnippetImprovement.objects.get(pk=improve_id)
	except:
		HttpResponseRedirect('/')

	# Update improved snippet table and code table
	improved_snippet.approve_date = timezone.now()
	improved_snippet.save()

	# Update Code table
	snippet = Code.objects.get(pk=improved_snippet.code.id)
	snippet.code = improved_snippet.new_code
	snippet.save()

	return HttpResponseRedirect(reverse('snippetmanager:mysnippets'))

# Disapprove a updated snippet
@login_required
def disapprove_snippet(request, improve_id):
	try:
		improved_snippet = SnippetImprovement.objects.get(pk=improve_id)
	except:
		HttpResponseRedirect('/')

	# Update improved snippet table
	improved_snippet.disapprove_date = timezone.now()
	improved_snippet.save()

	return HttpResponseRedirect(reverse('snippetmanager:mysnippets'))

# Facebook login
def facebook_login(request):
	facebook_id = request.GET.get('facebook_id')
	first_name = request.GET.get('first_name')
	last_name = request.GET.get('last_name')

	try:
		user = User.objects.create_user(facebook_id+'@facebook.com', facebook_id+'@facebook.com', 'facebookpass')
	except:
		try:
			facebook_login = FacebookLogin.objects.get(facebook_id=facebook_id)
		except:
			return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))

		user = authenticate(username=facebook_id+'@facebook.com', password='facebookpass')
		login(request, user)
		
		return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))

	user.first_name = first_name
	user.last_name = last_name
	user.save()

	facebook_user = User.objects.get(pk=user.id)
	facebook_login = FacebookLogin(facebook_id=facebook_id, user=facebook_user)

	facebook_login.save()

	user = authenticate(username=facebook_id+'@facebook.com', password='facebookpass')
	login(request, user)

	return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))

# Google Login
def google_login(request):
	google_id = request.GET.get('google_id')
	first_name = request.GET.get('first_name')
	last_name = request.GET.get('last_name')

	try:
		user = User.objects.create_user(google_id, google_id+'@google.com', 'googlepass')
	except:
		try:
			google_login = GoogleLogin.objects.get(google_id=google_id)
		except:
			return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))

		user = authenticate(username=google_id, password='googlepass')
		login(request, user)

		return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))

	user.first_name = first_name
	user.last_name = last_name
	user.save()

	google_user = User.objects.get(pk=user.id)
	google_login = GoogleLogin(google_id=google_id, user=google_user)

	google_login.save()

	user = authenticate(username=google_id, password='googlepass')
	login(request, user)

	return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))


