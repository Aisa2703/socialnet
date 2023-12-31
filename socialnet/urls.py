"""
URL configuration for socialnet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from core.views import *
from django.conf import settings  # !
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage),
    path('contacts/', contacts),
    path('about_us/', about_us),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('add_profile/', add_profile, name='add-profile'),
    path('category_info/', category_list, name='category-info'),
    path('category_object/<int:id>', category_detail),
    path('short_file/<int:id>/', short_file, name='short-info'),
    path('short_lst/', short_list, name='shorts-list'),
    path('saved_posts/', saved_posts_list, name='saved-posts'),
    path('user_posts/<int:id>/', user_posts, name='user-posts'),
    path('posts/', post_list, name='posts'),
    path('posts/<int:id>/', post_detail, name='post-detail'),
    path('update-post/<int:id>/', update_post, name='update-post'),
    path('add-post/', create_post, name='add-post'),
    path('delete-post/<int:id>/', delete_post, name='delete-post'),
    path('add-posts/', add_posts, name='add-posts'),
    path('add-short/', create_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('remove-saved/', remove_saved, name='remove-saved'),
    path('registration/', register, name='register'),
    path('users/', include('userapp.urls')),
    path('search/', search, name='search'),
    path('search-result/', search_result, name='search-result'),
    path('add-subscriber/<int:profile_id>/', add_subscriber, name='add-subscriber'),
    path('remove-follower/<int:profile_id>/', remove_follower, name='remove-follower'),
    path('notification/', notifications, name='notification'),
    path('comment-edit/<int:id>/', comment_edit, name='comment-edit'),
    path('comment-delete/<int:id>/', comment_delete, name='comment-delete'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
