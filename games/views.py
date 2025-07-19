import requests
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

COMPOSERS_TRACKS = [
    {
        "name": "Edvar Grieg",
        "track_ids": [473218992, 473219382]
    },
    {
        "name": "Ludwig van Beethoven",
        "track_ids": [473219002, 473219202, 473219232, 473219282, 473219432]
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
        "track_ids": [473219072, 473219122, 473219322, 473219402]
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
        "track_ids": [473219112, 473219192, 473219262, 473219312, 473219352, 473219362, 473219472]
    },
    {
        "name": "Jules Massenet",
        "track_ids": [473219132]
    },
    {
        "name": "Antonín Dvořák",
        "track_ids": [473219142, 473219322]
    },
    {
        "name": "Johann Strauss (Père)",
        "track_ids": [473219422]
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
        "track_ids": [473219222, 473219412]
    },
    {
        "name": "Jacques Offenbach",
        "track_ids": [473219242]
    },
    {
        "name": "Remo Giazotto",
        "track_ids": [473219252]
    },
    {
        "name": "Gioachino Rossini",
        "track_ids": [473219272]
    },
    {
        "name": "Bedřich Smetana",
        "track_ids": [473219292]
    },
    {
        "name": "Luigi Boccherini",
        "track_ids": [473219302]
    },
    {
        "name": "Jean Sibelius",
        "track_ids": [473219342]
    },    {
        "name": "George Frideric Handel",
        "track_ids": [473219372]
    },
    {
        "name": "Gabriel Fauré",
        "track_ids": [473219392]
    },
    {
        "name": "Stanley Myers",
        "track_ids": [473219442]
    },
    {
        "name": "Arcangelo Corelli,",
        "track_ids": [473219452]
    },
    {
        "name": "Sergueï Rachmaninov",
        "track_ids": [473219462]
    }
]


def get_all_deezer_tracks(tracklist_url):
    tracks = []
    while tracklist_url:
        response = requests.get(tracklist_url, timeout=10, verify=True)
    
        print("Get all deezer tracks status:", response.status_code)

        data = response.json()
        tracks.extend(data["data"])
        tracklist_url = data.get("next")
    return tracks


@require_GET
def get_deezer_album(request, album_id):
    response = requests.get(f"https://api.deezer.com/album/{album_id}", timeout=10, verify=True)
    
    print("Get deezer album status:", response.status_code)

    album = response.json()
    tracklist_url = album["tracklist"]
    tracks = get_all_deezer_tracks(tracklist_url)

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
            "preview": track["preview"],
            "composer": "Test"
        }

        # Find and add composer
        """
        composer_name = find_composer(track["id"])
        if composer_name:
            q["composer"] = composer_name
            
            # Add to list (only when composer found)
            quizz.append(q)
        """
        quizz.append(q)
        
    random.shuffle(quizz)
    return JsonResponse(quizz, safe=False)
