from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .models import Profile

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
    return JsonResponse({'message': 'Logged out'})

@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        return JsonResponse(
            {'username': request.user.username, 'email': request.user.email, 'nb_keys': profile.nb_keys}
        )
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
        errors = forms.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)

@ensure_csrf_cookie
@require_POST
@login_required
def add_keys(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        nb_keys_winned = int(data.get('nb_keys_winned'))
        if nb_keys_winned <= 0:
            return JsonResponse({"error": "nb_keys_winned must be > 0"}, status=400)
        
        profile = get_object_or_404(Profile, user=request.user)
        profile.nb_keys += nb_keys_winned
        profile.save(update_fields=["nb_keys"])

        return JsonResponse({"status": "success", "new_total": profile.nb_keys}, status=201)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)