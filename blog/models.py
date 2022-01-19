from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length=30)
	content = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	views = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.title
		
class Comment(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.content[0:50]
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='default.jpg')
	
	def __str__(self):
		return f'{self.user.username} profile'
	
	
             
            