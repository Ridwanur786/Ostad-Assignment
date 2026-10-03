from django.contrib import admin
from .models import Property, RentalRequest, Review


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'property_type',
        'location',
        'monthly_rent',
        'bedrooms',
        'bathrooms',
        'availability_status',
        'created_at',
    )
    list_filter = ('property_type', 'availability_status', 'created_at')
    search_fields = ('title', 'description', 'location', 'owner__username', 'owner__email')
    list_editable = ('availability_status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('property__title', 'tenant__username', 'tenant__email', 'message')
    list_editable = ('status',)
    date_hierarchy = 'request_date'
    ordering = ('-request_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('property__title', 'tenant__username', 'tenant__email', 'comment')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


