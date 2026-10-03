# Generated manually for properties app

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='e.g. Luxury 3-Bedroom Apartment in Gulshan', max_length=200)),
                ('description', models.TextField(help_text='Detailed description of features, amenities, and terms')),
                ('property_type', models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House / Villa'), ('condo', 'Condominium'), ('studio', 'Studio Apartment'), ('duplex', 'Duplex'), ('commercial', 'Commercial / Office Space'), ('room', 'Single Room / Flatshare')], default='apartment', help_text='Type of the property', max_length=50)),
                ('location', models.CharField(help_text='Location / City / Neighborhood (e.g. Dhanmondi Road 27, Dhaka)', max_length=255)),
                ('monthly_rent', models.DecimalField(decimal_places=2, help_text='Monthly rent amount (e.g. 25000.00)', max_digits=10)),
                ('bedrooms', models.PositiveIntegerField(default=1, help_text='Number of bedrooms')),
                ('bathrooms', models.PositiveIntegerField(default=1, help_text='Number of bathrooms')),
                ('image', models.ImageField(blank=True, help_text='Upload a representative photo of the property', null=True, upload_to='property_images/')),
                ('availability_status', models.CharField(choices=[('available', 'Available'), ('rented', 'Rented'), ('pending', 'Pending Approval'), ('maintenance', 'Under Maintenance')], default='available', help_text='Current availability status of the property', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(help_text='The owner of this property', on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ['-created_at'],
            },
        ),
    ]
