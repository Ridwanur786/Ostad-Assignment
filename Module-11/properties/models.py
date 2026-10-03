from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('room', 'Room'),
        ('office', 'Office'),
        ('condo', 'Condominium'),
        ('studio', 'Studio Apartment'),
        ('duplex', 'Duplex'),
        ('commercial', 'Commercial Space'),
    )

    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('pending', 'Pending Approval'),
        ('maintenance', 'Under Maintenance'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties',
        help_text="The owner of this property"
    )
    title = models.CharField(max_length=200, help_text="e.g. Luxury 3-Bedroom Apartment in Gulshan")
    description = models.TextField(help_text="Detailed description of features, amenities, and terms")
    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPE_CHOICES,
        default='apartment',
        help_text="Type of the property"
    )
    location = models.CharField(
        max_length=255,
        help_text="Location / City / Neighborhood (e.g. Dhanmondi Road 27, Dhaka)"
    )
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monthly rent amount (e.g. 25000.00)"
    )
    bedrooms = models.PositiveIntegerField(
        default=1,
        help_text="Number of bedrooms"
    )
    bathrooms = models.PositiveIntegerField(
        default=1,
        help_text="Number of bathrooms"
    )
    image = models.ImageField(
        upload_to='property_images/',
        blank=True,
        null=True,
        help_text="Upload a representative photo of the property"
    )
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available',
        help_text="Current availability status of the property"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} ({self.location}) - {self.get_property_type_display()}"

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    @property
    def is_available(self):
        return self.availability_status == 'available'

    @property
    def display_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # Elegant default property placeholder
        return "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&auto=format&fit=crop&q=80"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    @property
    def review_count(self):
        return self.reviews.count()


class RentalRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rental_requests'
    )
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rental_requests'
    )
    message = models.TextField(
        help_text="Inquiry message from tenant to property owner"
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Rental Request'
        verbose_name_plural = 'Rental Requests'

    def __str__(self):
        return f"Request by {self.tenant.username} for {self.property.title} ({self.get_status_display()})"


class Review(models.Model):
    RATING_CHOICES = (
        (5, '5 Stars - Excellent'),
        (4, '4 Stars - Very Good'),
        (3, '3 Stars - Good'),
        (2, '2 Stars - Fair'),
        (1, '1 Star - Poor'),
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(
        help_text="Review comment from tenant"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'tenant')
        verbose_name = 'Review & Rating'
        verbose_name_plural = 'Reviews & Ratings'

    def __str__(self):
        return f"Review by {self.tenant.username} for {self.property.title} ({self.rating}/5)"

