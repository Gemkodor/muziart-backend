import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from core.models import Profile
from .models import Quest, UserQuest


def quests_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    quests = Quest.objects.all()

    user_quests_map = {
        uq.quest_id: uq
        for uq in UserQuest.objects.filter(profile=profile)
    }

    data = []
    for quest in quests:
        uq = user_quests_map.get(quest.id)
        progress = uq.progress if uq else 0
        claimed = uq.claimed if uq else False
        data.append({
            'id': quest.id,
            'title': quest.title,
            'description': quest.description,
            'quest_type': quest.quest_type,
            'required_count': quest.required_count,
            'xp_reward': quest.xp_reward,
            'keys_reward': quest.keys_reward,
            'progress': progress,
            'completed': progress >= quest.required_count,
            'claimed': claimed,
        })

    return JsonResponse(data, safe=False)


def claim_quest(request, quest_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    profile = get_object_or_404(Profile, user=request.user)
    quest = get_object_or_404(Quest, id=quest_id)
    user_quest = get_object_or_404(UserQuest, profile=profile, quest=quest)

    if user_quest.claimed:
        return JsonResponse({'error': 'Already claimed'}, status=400)

    if user_quest.progress < quest.required_count:
        return JsonResponse({'error': 'Quest not completed yet'}, status=400)

    user_quest.claimed = True
    user_quest.claimed_at = timezone.now()
    user_quest.save()

    profile.experience += quest.xp_reward
    profile.add_keys(quest.keys_reward)
    profile.save()

    return JsonResponse({
        'message': 'Rewards claimed!',
        'xp_reward': quest.xp_reward,
        'keys_reward': quest.keys_reward,
        'updated_xp': profile.experience,
        'level': profile.get_level(),
        'progress': round(profile.get_progression_ratio(), 2),
        'nb_keys': profile.nb_keys,
    })
