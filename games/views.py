from django.http import JsonResponse
from django.templatetags.static import static
from games.models import Track, ScrollingGame, Instrument
from quests.progress import check_quest_progress
from daily.progress import complete_daily_activity
import json
import random

# Notes available per level. Each level adds notes progressively.
# Format: (note_name, octave)
LEVEL_NOTES = {
    # Portée — ancres visuelles
    1:  [('G', 4), ('A', 4)],
    2:  [('G', 4), ('A', 4), ('B', 4)],
    3:  [('F', 4), ('G', 4), ('A', 4), ('B', 4)],
    4:  [('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5)],
    5:  [('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5)],
    6:  [('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5)],
    7:  [('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5)],
    8:  [('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5)],
    # Lignes supplémentaires basses (Do central et en dessous)
    9:  [('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5)],
    10: [('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5)],
    # Lignes supplémentaires hautes (Sol5 et au-dessus)
    11: [('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5)],
    12: [('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5)],
    13: [('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5)],
    14: [('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5)],
    15: [('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6)],
    16: [('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6)],
    17: [('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6), ('D', 6)],
    18: [('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6), ('D', 6)],
    19: [('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6), ('D', 6), ('E', 6)],
    20: [('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4), ('A', 4), ('B', 4), ('C', 5), ('D', 5), ('E', 5), ('F', 5), ('G', 5), ('A', 5), ('B', 5), ('C', 6), ('D', 6), ('E', 6)],
}
MAX_LEVEL = max(LEVEL_NOTES.keys())

# Bass clef (clé de fa) — same progressive structure, anchored on F3 (line 4)
LEVEL_NOTES_BASS = {
    1:  [('F', 3), ('G', 3)],
    2:  [('E', 3), ('F', 3), ('G', 3)],
    3:  [('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    4:  [('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    5:  [('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    6:  [('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    7:  [('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    8:  [('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3)],
    9:  [('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3)],
    10: [('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4)],
    11: [('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4)],
    12: [('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4)],
    13: [('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4)],
    14: [('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4)],
    15: [('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4)],
    16: [('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4)],
    17: [('C', 2), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4)],
    18: [('C', 2), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4)],
    19: [('B', 1), ('C', 2), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4)],
    20: [('A', 1), ('B', 1), ('C', 2), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('A', 2), ('B', 2), ('C', 3), ('D', 3), ('E', 3), ('F', 3), ('G', 3), ('A', 3), ('B', 3), ('C', 4), ('D', 4), ('E', 4), ('F', 4), ('G', 4)],
}


def scrolling_game_level(request, clef, level_number):
    notes_map = LEVEL_NOTES_BASS if clef == 'bass' else LEVEL_NOTES
    clamped_level = min(int(level_number), MAX_LEVEL)
    allowed_notes = notes_map[clamped_level]

    return JsonResponse({
        'level_number': clamped_level,
        'notes': [{'note': note, 'octave': octave} for note, octave in allowed_notes]
    }, safe=False)


def end_scrolling_game_session(request):
    if request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        scrolling_game = ScrollingGame.objects.filter(profile=profile).first()
        
        if scrolling_game:
            data = json.loads(request.body.decode('utf-8'))
            score = data.get('score', 0)
            clef = data.get('clef', 'treble')

            if clef == 'bass':
                scrolling_game.nb_correct_answers_bass += score
                threshold = scrolling_game.current_level_bass * 50
                if scrolling_game.nb_correct_answers_bass >= threshold:
                    scrolling_game.current_level_bass += 1
                    scrolling_game.nb_correct_answers_bass -= threshold
            else:
                scrolling_game.nb_correct_answers += score
                threshold = scrolling_game.current_level * 50
                if scrolling_game.nb_correct_answers >= threshold:
                    scrolling_game.current_level += 1
                    scrolling_game.nb_correct_answers -= threshold

            scrolling_game.save()
            check_quest_progress(profile, 'play_notes_reading')
            complete_daily_activity(profile, 'notes_reading')
            return JsonResponse({
                'success': True,
                'current_level': scrolling_game.current_level,
                'score': scrolling_game.nb_correct_answers,
                'current_level_bass': scrolling_game.current_level_bass,
                'score_bass': scrolling_game.nb_correct_answers_bass,
            })
    
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