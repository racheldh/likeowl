from django.urls import path

from . import views

# Create your urls here.

urlpatterns = [
    path('',views.home, name='home'),
    path('contact', views.contact, name='contact'),
]
