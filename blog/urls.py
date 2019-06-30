from django.contrib import admin
from django.urls import path, include
import blog.views

urlpatterns = [
    path('home', blog.views.home, name='mypage'),
    path('posts/new/', blog.views.new, name='new'),
    path('post/<int:post_id>/edit', blog.views.edit, name='edit'),
    # path('post/<int:post_id>/remove', blog.views.remove, name='remove'),
    path('posts/<int:post_id>/newcomment/', blog.views.newcomment, name='newcomment'),
    path('posts/<slug:date>/', blog.views.detail, name='detail'),
    path('comment/<int:comment_id>/remove', blog.views.removecomment, name='removecomment'),
    path('board', blog.views.board, name='board'),
    
]

