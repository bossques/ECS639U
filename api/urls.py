"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from .views import main_spa, login_view, register_view, logout_view, profile_view, articles_view, article_view, category_view, comments_view, comment_view

urlpatterns = [
    path('', main_spa, name='home'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('api/profile/', profile_view, name='profile'),
    path('api/profile/categories/<int:category_id>/', category_view, name='category'),
    path('api/articles/', articles_view, name='articles'),
    path('api/articles/<int:article_id>/', article_view, name='article'),
    path('api/articles/<int:article_id>/comments/', comments_view, name='comments'),
    path('api/articles/<int:article_id>/comments/<int:comment_id>/', comment_view, name='comment')
]
