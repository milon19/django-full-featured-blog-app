from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.changed_data.get('username')
            messages.success(request, f'Welcome {username}! Login Here.')
            return redirect('')

    else:
        form = UserRegistrationForm
    return render(request, 'users/registration.html', {'form':form})