from django.shortcuts import render
from django import views
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from Account.forms import UserRegistrationForm


class UserRegistrationView(views.View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'Account/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'Account/register_done.html', {'new_user': new_user})
        return render(request, 'Account/register.html', {'form': form})