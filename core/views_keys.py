from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Profile
import json

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
    
    
def add_xp(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        experience_winned = int(data.get('xp_winned'))
        profile = get_object_or_404(Profile, user=request.user)
        profile.experience += experience_winned
        profile.save(update_fields=["experience"])
        return JsonResponse({
            'status': "success", 
            'level': profile.get_level(),
            'experience': profile.experience,
            'progress': round(profile.get_progression_ratio(), 2),
        }, status=201)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)