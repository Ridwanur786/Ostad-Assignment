from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list_view, name='property_list'),
    path('my-properties/', views.my_properties_view, name='my_properties'),
    path('requests/', views.my_rental_requests_view, name='my_rental_requests'),
    path('tenant-dashboard/', views.my_rental_requests_view, name='tenant_dashboard'),
    path('create/', views.property_create_view, name='property_create'),
    path('<int:pk>/', views.property_detail_view, name='property_detail'),
    path('<int:pk>/edit/', views.property_update_view, name='property_update'),
    path('<int:pk>/delete/', views.property_delete_view, name='property_delete'),
    path('<int:pk>/toggle-status/', views.property_toggle_status_view, name='property_toggle_status'),
    path('<int:pk>/request/', views.send_rental_request_view, name='send_rental_request'),
    path('requests/<int:pk>/cancel/', views.cancel_rental_request_view, name='cancel_rental_request'),
    path('requests/<int:pk>/<str:action>/', views.manage_rental_request_view, name='manage_rental_request'),
]

