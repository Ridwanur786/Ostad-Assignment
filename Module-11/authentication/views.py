from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import Profile


def home_view(request):
    """Landing page showcasing the Property Rental & Management System."""
    return render(request, 'home.html')


def register_view(request):
    """User registration view with role selection and profile creation."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role_display = user.profile.get_role_display()
            messages.success(
                request,
                f"Account created successfully for {user.username}! You are registered as a {role_display}."
            )
            # Log the user in immediately upon registration
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below to register.")
    else:
        form = UserRegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    """User login view supporting username or email login."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle "Remember Me"
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Browser close terminates session

            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials. Please check your username/email and password.")
    else:
        form = UserLoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    """User logout view supporting both GET and POST."""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"Goodbye, {username}! You have been logged out successfully.")
    return redirect('login')


@login_required
def profile_view(request):
    """Displays user profile details and role information."""
    # Ensure profile exists even if superuser was created via CLI
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'authentication/profile.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def profile_update_view(request):
    """Updates user information (name, email) and profile details (role, phone, address, photo)."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below to update your profile.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'authentication/profile_update.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    })


@login_required
def change_password_view(request):
    """Allows user to change their password securely."""
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below to change your password.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'authentication/change_password.html', {'form': form})
