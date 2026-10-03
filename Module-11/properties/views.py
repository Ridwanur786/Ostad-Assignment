from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Property, RentalRequest, Review
from .forms import PropertyForm, RentalRequestForm, ReviewForm
from authentication.models import Profile


def property_list_view(request):
    """
    Public listing of all properties.
    Supports multi-field search and filtering by property type, location, rent, bedrooms, and status.
    """
    queryset = Property.objects.select_related('owner', 'owner__profile').all()

    # Search query (title, description, location)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # Property type filter
    property_type = request.GET.get('property_type', '').strip()
    if property_type:
        queryset = queryset.filter(property_type=property_type)

    # Location filter
    location = request.GET.get('location', '').strip()
    if location:
        queryset = queryset.filter(location__icontains=location)

    # Minimum rent filter
    min_rent = request.GET.get('min_rent', '').strip()
    if min_rent:
        try:
            queryset = queryset.filter(monthly_rent__gte=float(min_rent))
        except ValueError:
            pass

    # Maximum rent filter
    max_rent = request.GET.get('max_rent', '').strip()
    if max_rent:
        try:
            queryset = queryset.filter(monthly_rent__lte=float(max_rent))
        except ValueError:
            pass

    # Bedrooms filter
    bedrooms = request.GET.get('bedrooms', '').strip()
    if bedrooms:
        try:
            queryset = queryset.filter(bedrooms__gte=int(bedrooms))
        except ValueError:
            pass

    # Availability filter (default: show all, or filter if specified)
    availability = request.GET.get('availability', '').strip()
    if availability:
        queryset = queryset.filter(availability_status=availability)

    # Pagination: 6 properties per page
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_count': queryset.count(),
        'search_query': search_query,
        'property_types': Property.PROPERTY_TYPE_CHOICES,
        'availability_choices': Property.AVAILABILITY_CHOICES,
        'selected_type': property_type,
        'selected_location': location,
        'selected_min_rent': min_rent,
        'selected_max_rent': max_rent,
        'selected_bedrooms': bedrooms,
        'selected_availability': availability,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail_view(request, pk):
    """
    Displays full details of a specific property.
    Includes specs, description, photo, owner details, rental request form, and reviews.
    RULES FOR REVIEWS:
    - Only tenants with an ACCEPTED rental request can submit a review.
    - A tenant can review a property ONLY ONCE.
    """
    property_obj = get_object_or_404(
        Property.objects.select_related('owner', 'owner__profile'),
        pk=pk
    )
    is_owner = request.user.is_authenticated and (property_obj.owner == request.user or request.user.is_superuser)

    # Check for existing rental request from the current logged-in user
    existing_request = None
    if request.user.is_authenticated and not is_owner:
        existing_request = RentalRequest.objects.filter(
            property=property_obj,
            tenant=request.user
        ).order_by('-request_date').first()

    request_form = RentalRequestForm()

    # Reviews and eligibility checks
    reviews = property_obj.reviews.select_related('tenant', 'tenant__profile').all()
    can_review = False
    has_reviewed = False
    user_review = None

    if request.user.is_authenticated and not is_owner:
        user_review = Review.objects.filter(property=property_obj, tenant=request.user).first()
        if user_review:
            has_reviewed = True
        else:
            # Check if tenant has an accepted rental request for this property
            has_accepted_request = RentalRequest.objects.filter(
                property=property_obj,
                tenant=request.user,
                status='accepted'
            ).exists()
            if has_accepted_request:
                can_review = True

    review_form = ReviewForm()

    # Fetch other listings from the same owner (max 3)
    related_properties = Property.objects.filter(owner=property_obj.owner).exclude(pk=property_obj.pk)[:3]

    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'is_owner': is_owner,
        'existing_request': existing_request,
        'request_form': request_form,
        'reviews': reviews,
        'can_review': can_review,
        'has_reviewed': has_reviewed,
        'user_review': user_review,
        'review_form': review_form,
        'related_properties': related_properties,
    })


@login_required
def add_review_view(request, pk):
    """
    Add a review and rating for a property.
    RULES:
    1. Must be logged in (@login_required).
    2. Tenant must have an ACCEPTED rental request for this property.
    3. Tenant can review a property ONLY ONCE.
    """
    property_obj = get_object_or_404(Property, pk=pk)

    # Rule: Tenant must have an accepted request
    has_accepted_request = RentalRequest.objects.filter(
        property=property_obj,
        tenant=request.user,
        status='accepted'
    ).exists()

    if not has_accepted_request and not request.user.is_superuser:
        messages.error(
            request,
            "Access Denied: You can only leave a review after your rental request has been accepted by the owner."
        )
        return redirect('property_detail', pk=pk)

    # Rule: Tenant can review only once
    if Review.objects.filter(property=property_obj, tenant=request.user).exists():
        messages.warning(request, "You have already submitted a review for this property.")
        return redirect('property_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property_obj
            review.tenant = request.user
            review.save()
            messages.success(request, "Thank you! Your review and rating have been posted.")
        else:
            messages.error(request, "Please provide a valid rating and review comment.")

    return redirect('property_detail', pk=pk)




@login_required
def property_create_view(request):
    """
    Create a new property listing.
    Restricted to Property Owners (or superusers).
    """
    # Verify user is a Property Owner
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not (profile.is_owner or request.user.is_superuser):
        messages.warning(
            request,
            "Only Property Owners can create new property listings. "
            "Please update your role to 'Property Owner' in your profile settings."
        )
        return redirect('profile_update')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_property = form.save(commit=False)
            new_property.owner = request.user
            new_property.save()
            messages.success(request, f"Property '{new_property.title}' created successfully!")
            return redirect('property_detail', pk=new_property.pk)
        else:
            messages.error(request, "Please correct the errors below to list your property.")
    else:
        form = PropertyForm()

    return render(request, 'properties/property_form.html', {
        'form': form,
        'title': 'Add New Property Listing',
        'button_text': 'Create Listing',
        'is_edit': False,
    })


@login_required
def property_update_view(request, pk):
    """
    Update an existing property listing.
    SECURITY CHECK: A user must NOT be able to edit another owner's property.
    """
    property_obj = get_object_or_404(Property, pk=pk)

    # Strictly verify ownership
    if property_obj.owner != request.user and not request.user.is_superuser:
        messages.error(request, "Access Denied: You do not have permission to edit another owner's property.")
        return HttpResponseForbidden("Access Denied: You cannot edit another owner's property.")

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Property '{property_obj.title}' updated successfully!")
            return redirect('property_detail', pk=property_obj.pk)
        else:
            messages.error(request, "Please correct the errors below to update your property.")
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'properties/property_form.html', {
        'form': form,
        'property': property_obj,
        'title': f'Edit Property: {property_obj.title}',
        'button_text': 'Save Changes',
        'is_edit': True,
    })


@login_required
def property_delete_view(request, pk):
    """
    Delete a property listing.
    SECURITY CHECK: A user must NOT be able to delete another owner's property.
    """
    property_obj = get_object_or_404(Property, pk=pk)

    # Strictly verify ownership
    if property_obj.owner != request.user and not request.user.is_superuser:
        messages.error(request, "Access Denied: You do not have permission to delete another owner's property.")
        return HttpResponseForbidden("Access Denied: You cannot delete another owner's property.")

    if request.method == 'POST':
        title = property_obj.title
        property_obj.delete()
        messages.success(request, f"Property '{title}' was deleted successfully.")
        return redirect('my_properties')

    return render(request, 'properties/property_confirm_delete.html', {
        'property': property_obj,
    })


@login_required
def my_properties_view(request):
    """
    Dashboard for property owners to manage their listings and rental requests.
    Displays metrics:
    1. Total properties
    2. Available properties
    3. Total rental requests
    4. Pending requests
    5. Accepted requests
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not (profile.is_owner or request.user.is_superuser):
        messages.info(
            request,
            "You are currently registered as a Tenant. Switch your role to 'Property Owner' in your profile to list properties."
        )

    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    received_requests = RentalRequest.objects.filter(property__owner=request.user).select_related('tenant', 'property').order_by('-request_date')

    # Metrics specified for Owner Dashboard
    total_properties = properties.count()
    available_properties = properties.filter(availability_status='available').count()
    total_rental_requests = received_requests.count()
    pending_requests = received_requests.filter(status='pending').count()
    accepted_requests = received_requests.filter(status='accepted').count()

    return render(request, 'properties/my_properties.html', {
        'properties': properties,
        'received_requests': received_requests,
        'total_properties': total_properties,
        'available_properties': available_properties,
        'total_rental_requests': total_rental_requests,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
    })



@login_required
def property_toggle_status_view(request, pk):
    """
    Quickly toggle the availability status between 'available' and 'rented'.
    Only callable by the property owner.
    """
    if request.method != 'POST':
        return redirect('property_detail', pk=pk)

    property_obj = get_object_or_404(Property, pk=pk)

    # Strictly verify ownership
    if property_obj.owner != request.user and not request.user.is_superuser:
        messages.error(request, "Access Denied: You cannot modify this property.")
        return HttpResponseForbidden("Access Denied.")

    if property_obj.availability_status == 'available':
        property_obj.availability_status = 'rented'
    else:
        property_obj.availability_status = 'available'
    property_obj.save()

    messages.success(
        request,
        f"Status for '{property_obj.title}' updated to {property_obj.get_availability_status_display()}."
    )

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('my_properties')


@login_required
def send_rental_request_view(request, pk):
    """
    Send a rental request for an available property.
    RULES:
    1. Must be logged in (@login_required).
    2. Cannot request own property.
    3. Cannot send multiple pending requests for the same property.
    """
    property_obj = get_object_or_404(Property, pk=pk)

    # Rule: Cannot request own property
    if property_obj.owner == request.user:
        messages.error(request, "Rule Violation: You cannot send a rental request for your own property.")
        return redirect('property_detail', pk=pk)

    # Rule: Cannot send multiple pending requests for the same property
    existing_pending = RentalRequest.objects.filter(
        property=property_obj,
        tenant=request.user,
        status='pending'
    ).first()
    if existing_pending:
        messages.warning(request, "You already have a pending rental request for this property.")
        return redirect('property_detail', pk=pk)

    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_req = form.save(commit=False)
            rental_req.property = property_obj
            rental_req.tenant = request.user
            rental_req.status = 'pending'
            rental_req.save()
            messages.success(
                request,
                f"Your rental request for '{property_obj.title}' has been submitted to the owner!"
            )
        else:
            messages.error(request, "Please enter a valid message for your request.")

    return redirect('property_detail', pk=pk)


@login_required
def cancel_rental_request_view(request, pk):
    """
    Cancel a pending rental request.
    RULES:
    1. Only the tenant who sent the request can cancel it.
    2. Only 'pending' requests can be cancelled.
    """
    rental_req = get_object_or_404(RentalRequest, pk=pk)

    # Rule: Only tenant who created request can cancel
    if rental_req.tenant != request.user and not request.user.is_superuser:
        messages.error(request, "Access Denied: You cannot cancel another user's rental request.")
        return HttpResponseForbidden("Access Denied.")

    # Rule: Only pending requests can be cancelled
    if rental_req.status != 'pending':
        messages.warning(request, f"Cannot cancel request as its status is '{rental_req.get_status_display()}'.")
        return redirect('my_rental_requests')

    if request.method == 'POST':
        rental_req.status = 'cancelled'
        rental_req.save()
        messages.success(request, f"Rental request for '{rental_req.property.title}' has been cancelled.")

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('my_rental_requests')


@login_required
def manage_rental_request_view(request, pk, action):
    """
    Accept or Reject a rental request.
    RULES:
    1. Only the property owner can accept or reject requests.
    """
    rental_req = get_object_or_404(RentalRequest, pk=pk)

    # Rule: Only property owner can accept/reject
    if rental_req.property.owner != request.user and not request.user.is_superuser:
        messages.error(request, "Access Denied: Only the property owner can accept or reject requests.")
        return HttpResponseForbidden("Access Denied.")

    if request.method == 'POST':
        if action == 'accept':
            rental_req.status = 'accepted'
            rental_req.save()
            messages.success(
                request,
                f"Rental request from {rental_req.tenant.first_name or rental_req.tenant.username} has been ACCEPTED!"
            )
        elif action == 'reject':
            rental_req.status = 'rejected'
            rental_req.save()
            messages.info(
                request,
                f"Rental request from {rental_req.tenant.first_name or rental_req.tenant.username} has been REJECTED."
            )

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('my_rental_requests')


@login_required
def my_rental_requests_view(request):
    """
    Tenant & Owner Dashboard for managing rental requests.
    Calculates Tenant Dashboard metrics:
    - Total rental requests
    - Pending requests
    - Accepted requests
    - Rejected requests
    """
    sent_requests = RentalRequest.objects.filter(tenant=request.user).select_related('property', 'property__owner').order_by('-request_date')
    received_requests = RentalRequest.objects.filter(property__owner=request.user).select_related('tenant', 'property').order_by('-request_date')

    # Tenant Dashboard Metrics
    total_sent_requests = sent_requests.count()
    pending_sent_requests = sent_requests.filter(status='pending').count()
    accepted_sent_requests = sent_requests.filter(status='accepted').count()
    rejected_sent_requests = sent_requests.filter(status='rejected').count()

    # Owner Received Requests Metrics
    pending_received_count = received_requests.filter(status='pending').count()

    return render(request, 'properties/my_rental_requests.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'total_sent_requests': total_sent_requests,
        'pending_sent_requests': pending_sent_requests,
        'accepted_sent_requests': accepted_sent_requests,
        'rejected_sent_requests': rejected_sent_requests,
        'pending_received_count': pending_received_count,
    })


