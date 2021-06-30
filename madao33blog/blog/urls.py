from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    path('post/<int:pk>/', views.post, name='post'),
    path('category/<str:cat>/', views.category_detail, name='category'),
    path('tags/<str:tag>/', views.tag, name='tag'),
]