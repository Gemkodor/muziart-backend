from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Profile, Card, ProfileCard, CollectionCategory
import json

def get_cards(request):
    category = request.GET.get('category')  # ex: "composer" ou "instrument"

    if not category:
        return JsonResponse({'error': 'Missing category parameter'}, status=400)

    try:
        category_obj = CollectionCategory.objects.get(name=category)
    except CollectionCategory.DoesNotExist:
        return JsonResponse({'error': 'Invalid category'}, status=400)
    
    # Get cards from category requested
    cards = Card.objects.filter(category=category_obj)
    
    # Check cards are unlocked by user
    user_profile = get_object_or_404(Profile, user=request.user)
    unlocked_card_ids = ProfileCard.objects.filter(
        profile=user_profile, 
        card__category=category_obj
    ).values_list('card_id', flat=True)
    
    data = []
    for card in cards:
        data.append({
            'id': card.id,
            'name': card.name,
            'image_name': card.image_name,
            'category': card.category.name,
            'description': card.description,
            'rarity': card.rarity.name,
            'unlocked': card.id in unlocked_card_ids,
            'priceToUnlock': card.price_to_unlock
        })
    
    return JsonResponse({
        'cards': data, 
        'nb_cards_unlocked': len(unlocked_card_ids)
    })

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