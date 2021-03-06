# Create your views here.
from blog.models import *
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import datetime
from django.template import RequestContext
from django.contrib.auth import login as django_login

def showpost(request):
	p_id = request.GET['post_id']
	post = Post.objects.get(id = p_id)
	comments = Comment.objects.filter(post = post).order_by('date').reverse()
	return render(request, 'showpost.html', {'post': post, 'comments': comments, 'request': request})

def home(request):
	return render(request, 'base.html')

def add_comment(request, post_id):
	user = request.user
	content = request.GET['content']
	post = Post.objects.get(pk = post_id)
	Comment.objects.create(commentor = user, content = content, post = post, date = datetime.datetime.now())
	return HttpResponseRedirect("/showpost?post_id="+str(post_id))

def add_blog(request):
	Blog.objects.create(owner = request.user)
	return HttpResponseRedirect("/profile?user_id="+str(request.user.id))

def add_blog_view(request):
	return render(request, 'addblog.html', {})

def add_post_view(request):
	return render(request, 'addpost.html', {})

def add_post(request):
	try:
		blog = Blog.objects.get(owner = request.user)
		Post.objects.create(blog = blog, description = request.GET['description'], title = request.GET['title'], date=datetime.datetime.now())
		return HttpResponseRedirect("/profile?user_id="+str(request.user.id))
	except:
		return HttpResponseRedirect("/profile?user_id="+str(request.user.id))

def login(request):
	try:
		mail = request.POST['email']
		password = request.POST['password']
	except:
		LoginError = True
		return render_to_response ('home.html',{"LoginError":LoginError},context_instance=RequestContext(request))
	authenticated_user = authenticate(email = mail, password = password)
	if authenticated_user is not None:
		django_login(request, authenticated_user)
		return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))
	else:
		LoginError = True
		return render_to_response ('home.html',{"LoginError":LoginError},context_instance=RequestContext(request))

def delete_post(request):
	Post.objects.get(pk = request.GET['post_id']).delete()
	return HttpResponseRedirect("/main")

def view_profile(request):
	user = MyUser.objects.get(pk = request.GET['user_id'])
	try:
		blog = Blog.objects.get(owner = user)
		posts = Post.objects.filter(blog = blog)
		return render(request, 'home.html',{'posts': posts, 'user': user, 'request': request})
	except:
		return render(request, 'home.html',{'none': "You have no blogs", 'user': user, 'request': request})

def main(request):
	all_posts = Post.objects.all().order_by('date').reverse()
	return render(request, 'main.html', {'all_posts': all_posts})

def edit_post(request):
	description = request.GET['description']
	title = request.GET['title']
	post = Post.objects.get(pk = request.GET['id'])
	post.description = description
	post.title = title
	post.save()
	return render(request, 'showpost.html', {'post': post})