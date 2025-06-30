import requests
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET


COMPOSERS_TRACKS = [
    {
        "name": "Edvar Grieg",
        "track_ids": [473218992]
    },
    {
        "name": "Ludwig van Beethoven",
        "track_ids": [473219002, 473219202, 473219232]
    },
    {
        "name": "Antonio Vivaldi",
        "track_ids": [473219012]
    },
    {
        "name": "Samuel Barber",
        "track_ids": [473219022]
    },
    {
        "name": "Richard Wagner",
        "track_ids": [473219032]
    },
    {
        "name": "Frédéric Chopin",
        "track_ids": [473219042]
    },
    {
        "name": "Johann Pachelbel",
        "track_ids": [473219052]
    },
    {
        "name": "Carl Orff",
        "track_ids": [473219062]
    },
    {
        "name": "Johann Sebastian Bach",
        "track_ids": [473219072, 473219122]
    },
    {
        "name": "Gustav Holst",
        "track_ids": [473219082]
    },
    {
        "name": "Claude Debussy",
        "track_ids": [473219092]
    },
    {
        "name": "Giuseppe Verdi",
        "track_ids": [473219102]
    },
    {
        "name": "Wolfgang Amadeus Mozart",
        "track_ids": [473219112, 473219192]
    },
    {
        "name": "Jules Massenet",
        "track_ids": [473219132]
    },
    {
        "name": "Antonín Dvořák",
        "track_ids": [473219142]
    },
    {
        "name": "Johann Strauss II",
        "track_ids": [473219152]
    },
    {
        "name": "Johannes Brahms",
        "track_ids": [473219162]
    },
    {
        "name": "Piotr Ilitch Tchaïkovski",
        "track_ids": [473219172]
    },
    {
        "name": "Erik Satie",
        "track_ids": [473219182]
    },
    {
        "name": "Edward Elgar",
        "track_ids": [473219212]
    },
    {
        "name": "Georges Bizet",
        "track_ids": [473219222]
    }
]

@require_GET
def deezer_albums(request, album_id):
    url = f"https://api.deezer.com/album/{album_id}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except requests.RequestException as exc:
        return JsonResponse(
            {"error": "Deezer API unavailable", "detail": str(exc)}, status=502
        )

    album = r.json()
    tracks = album.get("tracks", {}).get("data", [])

    def find_composer(track_id):
        for composer in COMPOSERS_TRACKS:
            if track_id in composer["track_ids"]:
                return composer["name"]

    quizz = []
    for track in tracks:
        # Create question
        q = {
            "id": track["id"],
            "title": track["title"],
            "preview": track["preview"]
        }

        # Find and add composer
        composer_name = find_composer(track["id"])
        if composer_name:
            q["composer"] = composer_name

        # Add to list
        quizz.append(q)

    random.shuffle(quizz)
    return JsonResponse(quizz, safe=False)