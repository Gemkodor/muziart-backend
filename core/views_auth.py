from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os

from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .models import Profile

def index(request):
    frontend_url = os.environ.get("FRONTEND_URL")

    return render(request, 'core/index.html', {'frontend_url': frontend_url})

@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend
    """
    return JsonResponse({'message': 'CSRF cookie set'})

@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        password = data['password']
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON'}, status=400
        )

    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )

def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out'})

@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'level': profile.get_level(),
            'experience': profile.experience,
            'progress': round(profile.get_progression_ratio(), 2),
            'nbKeys': profile.nb_keys
        }
        return JsonResponse(data)
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )

@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)