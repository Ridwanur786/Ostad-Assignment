from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:id>/', views.report_detail, name='report_detail'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:id>/edit/', views.report_update, name='report_update'),
    path('reports/<int:id>/delete/', views.report_delete, name='report_delete'),
    path('reports/<int:id>/resolve/', views.mark_resolved, name='mark_resolved'),
]