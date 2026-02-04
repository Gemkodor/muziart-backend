from django.http import JsonResponse
from .models import  Instrument, ScrollingGameLevel


def instruments_list(request):
    instruments = Instrument.objects.all().order_by('?')[:10].values()
    return JsonResponse(list(instruments), safe=False)


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