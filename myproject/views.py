import uuid
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .login_form import LoginForm
from .forms import RegisterForm

# Endpoint GET para retornar apenas o CSRF token e sessionid
@require_GET
def api_csrf_token(request):
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    return JsonResponse({'csrf': csrf_token, 'sessionid': session_id})

# Endpoint RESTful para login
@require_POST
def api_login(request):
    from django.middleware.csrf import get_token
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    csrf_token = get_token(request)
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    if user is not None:
        request.session.flush()  # Clear session and create new session key
        request.session.create() # Ensure a new session is created
        login(request, user)     # Authenticate the user for this session
        session_id = request.session.session_key
        return JsonResponse({
            'success': True,
            'csrf': csrf_token,
            'sessionid': session_id,
        })
    else:
        return JsonResponse({'success': False, 'error': 'Credenciais inválidas', 'csrf': csrf_token, 'sessionid': session_id}, status=401)
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

def testelogin(request):
    from django.middleware.csrf import get_token
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        csrf_token = get_token(request)
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        if user is not None:
            token = str(uuid.uuid4())
            return JsonResponse({
                'success': True,
                'username': user.username,
                'token': token,
                'email': user.email,
                'csrf': csrf_token,
                'sessionid': session_id,
            })
        else:
            return JsonResponse({'success': False, 'error': 'Credenciais inválidas', 'csrf': csrf_token, 'sessionid': session_id}, status=401)
    csrf_token = get_token(request)
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    return JsonResponse({'error': 'Método não permitido', 'csrf': csrf_token, 'sessionid': session_id}, status=405)

# View para renderizar a tela de teste do login
def testelogin_screen(request):
    return render(request, 'testelogin.html')