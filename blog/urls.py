from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
     path('', views.home, name="home"),
    path('blog/<str:id>/', views.blog, name="blog"),
    path('blog/<str:id>/details/', views.blog_details,name="blog_details"),
    path('blog/create/new/', views.create_blog, name="create_blog"),
    path('blog/<str:id>/edit/', views.edit_blog, name="edit_blog"),
    path('profile/<str:owner>/', views.profile, name="profile"),
    
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.registeruser, name="register"),
   
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
