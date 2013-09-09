###############################
# Home Views Controller
###############################

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django import forms
from django.contrib.auth.models import User

from snippetmanager.models import Points

class SigninForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length=12)

class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=75)
	password = forms.CharField(max_length=128)

# Home Page
def home(request):
	context = {
		'page': 'home'
	}

	return render(request, 'home.html', context)

# Sign Up Page
def sign_up(request):
	context = {
		'page': 'signup'
	}

	if request.method == 'POST':
		form = SignupForm(request.POST)

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			if password == password2:
				# check duplicate
				try:
					is_user = User.objects.get(email=email)
					context.update({'error_code': 2})
				except User.DoesNotExist:
					# start signing up user
					user = User.objects.create_user(email, email, password)
					user.first_name = first_name
					user.last_name = last_name
					user.save()

					# login user
					user = authenticate(username=email, password=password)
					login(request, user)

					return HttpResponseRedirect(reverse('snippetmanager:snippetworld'))
			else:
				context.update({'error_code': 1})
		else:
			posted_value = {
				'first_name': first_name,
				'last_name': last_name,
				'email': email,
				'password': password
			}
			context.update(posted_value)
	else:
		form = SignupForm()

	context.update({'form': form})

	return render(request, 'sign_up.html', context)

# Sign In Page
def sign_in(request):
	context = {
		'page': 'signin'
	}

	if request.method == 'POST':
		form = SigninForm(request.POST)

		email = request.POST['email']
		password = request.POST['password']

		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(username=email, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/')
				else:
					context['signin_error'] = 'The account has been disabled...'
					#data = {'status': 'no active'}
					#return HttpResponse(simplejson.dumps(data), mimetype='application/json')
			else:
				context['signin_error'] = 'Wrong username or password...'
				#data = {'status': 'no such user'}
				#return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	else:
		form = SigninForm()

	context.update({'form': form})

	return render(request, 'sign_in.html', context)

# Sign Out
def sign_out(request):
	logout(request)

	return redirect('/social_signout')

# Social Netowrk Sign out
def social_signout(request):
	context = {
		'page': 'social_signout'
	}

	return render(request, 'social_signout.html', context)