from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Registration successful. Welcome!'
            )

            return redirect('home')

    else:
        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )