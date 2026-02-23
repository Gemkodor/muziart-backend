from django.http import JsonResponse
from django.templatetags.static import static
from games.models import Track, ScrollingGame, ScrollingGameLevel, Instrument
import json

def scrolling_game_level(request, level_number):
    level = ScrollingGameLevel.objects.get(level_number=level_number)
    
    notes = [
        {
            "note": note.note.name,
            "octave": note.position
        }
        for note in level.notes.select_related("note")
    ]
    
    return JsonResponse({
        'level_number': level.level_number,
        'notes': notes
    }, safe=False)


def end_scrolling_game_session(request):
    if request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        scrolling_game = ScrollingGame.objects.filter(profile=profile).first()
        
        if scrolling_game:
            data = json.loads(request.body.decode('utf-8'))
            score = data.get('score', 0)
            scrolling_game.nb_correct_answers += score
            
            # Update current level if nb of correct answers is above 1000
            if scrolling_game.nb_correct_answers >= 1000:
                scrolling_game.current_level += 1
            
            scrolling_game.save()
            return JsonResponse({'success': True, 'current_level': scrolling_game.current_level, 'score': scrolling_game.nb_correct_answers})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def instruments_list(request):
    instruments = Instrument.objects.all().order_by('?')[:10].values()
    return JsonResponse(list(instruments), safe=False)


def random_track(request, nb_questions):
    tracks = Track.objects.order_by("?")[:nb_questions]
    data = [
        {
            "url": request.build_absolute_uri(static(f"audio/{track.filename}")),
            "title": track.title,
            "secondary_title": track.secondary_title,
            "composer":track.composer,
            "difficulty": track.difficulty
        }
        for track in tracks
    ]
    return JsonResponse(data, safe=False)