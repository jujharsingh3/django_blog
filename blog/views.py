#pylint:disable=E1101
from django.shortcuts import render, redirect, reverse
from .models import Blog, Comment
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
@login_required()
def home(request):
	search = request.GET.get('q')
	if search:
		blogs = Blog.objects.filter(
		Q(title__icontains=search) |
Q(owner__username__icontains=search)
		).order_by("-created_at")
	else:
		blogs =  Blog.objects.all().order_by("-created_at")
		
	context ={
		'blogs': blogs,
		'search': search
	}
	return render(request, 'blog/home.html', context)

@login_required()		
def blog(request, id):
	blog = Blog.objects.get(id=id)
	blog.views = blog.views + 1
	blog.save()
	
	comments = Comment.objects.filter(blog=blog).order_by('-created_at')
	if request.method == 'POST':
		content = request.POST.get('comment')
		comment = Comment.objects.create(user=request.user, blog=blog, content=content)
		comment.save()
		messages.success(request, 'Comment posted')
		return redirect(reverse("blog",kwargs={'id':str(blog.id)}))
	context = {
	'blog':blog,
	'comments':comments
	}
	return render(request, 'blog/blog.html', context)	
	
@login_required()	
def blog_details(request, id):
	blog = Blog.objects.get(id=id)
	comments = Comment.objects.filter(blog=blog)
	comments_count = comments.count
	if request.method == 'POST':
		blog.delete()
		messages.success(request, 'Blog deleted')
		return redirect('home')
	else:
		print("error")
	context = {
	'blog':blog,
	'comments_count':comments_count
	}
	return render(request, 'blog/details.html', context)

@login_required()	
def create_blog(request):
	if request.method == "POST":
		title = request.POST.get('title')
		content = request.POST.get('content')
		owner = request.user
		blog = Blog.objects.create(title=title, content=content, owner=owner)
		blog.save()
		messages.success(request, 'Blog created')
		return redirect(reverse("blog",kwargs={'id':str(blog.id)}))
	else:
		blog = None
	context ={
	'blog': blog
	}
	return render(request, 'blog/create_blog.html', context)	

@login_required()	
def edit_blog(request, id):
	blog = Blog.objects.get(id=id)
	if request.method == "POST":
		title = request.POST.get('title')
		content = request.POST.get('content')
		blog.title = title
		blog.content = content
		blog.save()
		messages.success(request, 'Blog updated')
		return redirect(reverse("blog",kwargs={'id':str(blog.id)}))
	context={
	'blog':blog,
	
	}
	return render(request, 'blog/edit_blog.html', context)

@login_required()
def profile(request, owner):
	blogs = Blog.objects.filter(owner__username=owner)
	user = User.objects.get(username=owner)
	if request.method == 'POST':
		user.username = request.POST.get('uname')
		user.email = request.POST.get('email')
		files = request.FILES
		print(len(files))
		if len(files) != 0:
			user.profile.avatar = files.get('image')
		
		user.save()
		messages.success(request, 'Profile updated login to continue')
		return redirect('login')
	context={
	'blogs':blogs,
	'user':user
	}
	return render(request, 'blog/profile.html', context)



def loginuser(request):
	if request.method == 'POST':
		uname = request.POST.get('uname')
		password = request.POST.get('password')
		user = authenticate(username=uname, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Successfully logged in')
			return redirect ('/')
		else:
			messages.error(request, 'User does not exists')
			return render(request, 'blog/login.html')
	return render(request, 'blog/login.html')

def logoutuser(request):
	logout(request)
	messages.success(request, 'Successfully logged out')
	return redirect('/login')
	
def registeruser(request):
	if request.method == 'POST':
		username = request.POST.get('uname')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		if password==password2:
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Username taken')
			else:
				user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
				user.save()
				messages.success(request, 'User successfully registered, Login to continue')
				return redirect('login')
	return render(request, 'blog/register.html')

