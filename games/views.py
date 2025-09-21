from django.http import JsonResponse
from django.templatetags.static import static
from .models import Track

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