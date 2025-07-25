from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Profile, Card, ProfileCard
import json

def get_cards(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_cards = ProfileCard.objects.filter(profile=profile).values_list('card_id', flat=True)
    cards = Card.objects.all()
    data = []
    
    for card in cards:
        data.append({
            'id': card.id,
            'name': card.name,
            'image_name': card.image_name,
            'category': card.category.name,
            'rarity': card.rarity.name,
            'unlocked': card.id in user_cards,
            'priceToUnlock': card.price_to_unlock
        })
    
    return JsonResponse({'cards': data, 'nb_cards_unlocked': len(user_cards)})

@csrf_exempt
@login_required
@require_POST
def unlock_card(request):
    body = json.loads(request.body)
    card_id = body.get('card_id')
    
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Carte introuvable'}, status=404)
    
    # Check if user has enough keys to unlock card
    profile = get_object_or_404(Profile, user=request.user)
    if profile.nb_keys < card.price_to_unlock:
        return JsonResponse({'error': 'Pas assez de clés'}, status=400)
    
    # Unlock card
    ProfileCard.objects.get_or_create(profile=profile, card=card)
    
    # Decrement number of keys
    profile.nb_keys -= card.price_to_unlock
    profile.save(update_fields=["nb_keys"])
    
    return JsonResponse({'success': True, 'message': f'Carte {card.name} débloquée !', 'new_total_keys': profile.nb_keys})