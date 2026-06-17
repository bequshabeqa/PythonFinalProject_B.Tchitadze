"""
URL configuration for web_Beka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import (
    about_view, 
    home_view, 
    product_view, 
    delete_comment, 
    HomeView, 
    logout_view, 
    login_view,
    register_view,
    blog_view,
    contact_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', about_view, name='about'),
    path('blog/', blog_view, name='blog'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),    
    path('product/<int:pk>/', product_view, name='product_detail'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact_view, name='contact'),
]
