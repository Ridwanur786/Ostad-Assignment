from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
]