from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth import authenticate
from .login_form import LoginForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/admin/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class GroupForm(forms.Form):
    name = forms.CharField(label='Group Name')
    data = forms.DateField(label='Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            group, created = Group.objects.get_or_create(name=name)
            return render(request, 'group_result.html', {'group': group, 'created': created})
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/create-group/')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
