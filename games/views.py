import requests
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

COMPOSERS_TRACKS = [
    {
        "name": "Edvar Grieg",
        "track_titles": [
            "Peer Gynt Suite No. 1, Op. 46: Morning Mood",
            "Peer Gynt Suite No. 1, Op. 46: Dans Le Château Du Roi De La Montagne"
        ]
    },
    {
        "name": "Ludwig van Beethoven",
        "track_titles": [
            "Symphonie No. 5 en Ut Mineur, Op. 67, \"Destin\": Allegro con brio",
            "Bagatelle en La Mineur, WoO 59, \"La Lettre à Elise\"",
            "Symphonie No. 9 en Ré Mineur, Op. 125, \"Chorale\": Ode à la joie",
            "Sonate No. 14 en Do Dièse Mineur pour Piano, Op. 27:2, \"Sonate au Clair de Lune\": Adagio sostenuto",
            "Egmont, Op. 84: Ouverture en Fa Mineur"
        ]
    },
    {
        "name": "Antonio Vivaldi",
        "track_titles": [
            "Le quattro stagioni (Les Quatre Saisons), Op. 8 - Concerto No. 1 en Mi Majeur, RV 269, \"La primavera\" (Le Printemps): I. Allegro"
        ]
    },
    {
        "name": "Samuel Barber",
        "track_titles": [
            "Adagio pour Cordes, Op. 11a"
        ]
    },
    {
        "name": "Richard Wagner",
        "track_titles": [
            "Die Walkürie (Les Valkyries), Act 3: La Chevauchée des Valkyries"
        ]
    },
    {
        "name": "Frédéric Chopin",
        "track_titles": [
            "Nocturnes, Op. 9: No. 2 en Mi Bémol Majeur"
        ]
    },
    {
        "name": "Johann Pachelbel",
        "track_titles": [
            "Canon en Ré Majeur"
        ]
    },
    {
        "name": "Carl Orff",
        "track_titles": [
            "Carmina Burana: O Fortuna"
        ]
    },
    {
        "name": "Johann Sebastian Bach",
        "track_titles": [
            "Suite pour Orchestre No. 3 en Ré Majeur, BWV 1068: Air",
            "Concerto Brandebourgeois No. 3 en Sol Majeur, BWV 1048: Allegro",
            "Ave Maria (d'après J.S. Bach)",
            "Double Concerto en Ré Mineur pour Deux Violons, BWV 1043: Vivace"
        ]
    },
    {
        "name": "Gustav Holst",
        "track_titles": [
            "Les Planètes, Op. 32: Jupiter, Celui Qui Apporte la Gaieté"
        ]
    },
    {
        "name": "Claude Debussy",
        "track_titles": [
            "Suite bergamasque, L 75: Clair de lune"
        ]
    },
    {
        "name": "Giuseppe Verdi",
        "track_titles": [
            "Nabucco: Le Choeur des Hébreux, \"Va pensiero, sull'ali dorate\""
        ]
    },
    {
        "name": "Wolfgang Amadeus Mozart",
        "track_titles": [
            "Concerto No. 21 en Ut Majeur pour Piano et Orchestre, K. 467: Andante",
            "Requiem, K. 626: Lacrimosa dies illa",
            "Die Zauberflöte (La Flute Enchantée), K. 620: Ouverture",
            "Symphonie No. 40 en Sol Mineur, K. 550: Allegro molto",
            "Sérénade No. 13 en Sol Majeur, K. 525, \"Une Petite Musique de Nuit\": Allegro",
            "Sonate pour Piano No. 11 en La Majeur, K. 331: Rondo: Alla turca",
            "Messe de Requiem: Dies irae - Tuba mirum"
        ]
    },
    {
        "name": "Jules Massenet",
        "track_titles": [
            "Thaïs: Méditation",
        ]
    },
    {
        "name": "Antonín Dvořák",
        "track_titles": [
            "Symphonie No. 9 en Mi Mineur, Op. 95, \"Du Nouveau Monde\": Largo",
            "Danse Slave No. 2 en Mi Mineur, Op. 72"
        ]
    },
    {
        "name": "Johann Strauss (Père)",
        "track_titles": [
            "La Marche de Radetzky, Op. 228"
        ]
    },
    {
        "name": "Johann Strauss II",
        "track_titles": [
            "An der schönen blauen Donau (Sur Le Beau Danube Bleu), Op. 314"
        ]
    },
    {
        "name": "Johannes Brahms",
        "track_titles": [
            "Danse Hongroise No. 5 en Sol Mineur"
        ]
    },
    {
        "name": "Piotr Ilitch Tchaïkovski",
        "track_titles": [
            "Suite du Lac des Cygnes, Op. 20: Scène"
        ]
    },
    {
        "name": "Erik Satie",
        "track_titles": [
            "Gymnopédie No. 1"
        ]
    },
    {
        "name": "Edward Elgar",
        "track_titles": [
            "Pomp and Circumstance, Op. 39: Land of Hope and Glory"
        ]
    },
    {
        "name": "Georges Bizet",
        "track_titles": [
            "Carmen Suite No. 2: Habanera",
            "L'Arlésienne Suite No. 1: Prélude"
        ]
    },
    {
        "name": "Jacques Offenbach",
        "track_titles": [
            "Les contes d'Hoffmann : Barcarolle"
        ]
    },
    {
        "name": "Remo Giazotto",
        "track_titles": [
            "Adagio en Sol Mineur pour Orchestre à Cordes et Orgue, \"Adagio d'Albinoni\""
        ]
    },
    {
        "name": "Gioachino Rossini",
        "track_titles": [
            "Il barbiere di Siviglia (Le Barbier de Seville): Ouverture"
        ]
    },
    {
        "name": "Bedřich Smetana",
        "track_titles": [
            "Má Vlast (Ma Patrie): Vltava (La Rivière Moldau)"    
        ]
    },
    {
        "name": "Luigi Boccherini",
        "track_titles": [
            "Quintette à Cordes en Mi Majeur, Op. 13: Minuet"
        ]
    },
    {
        "name": "Jean Sibelius",
        "track_titles": ["Finlandia, Op. 26"]
    },    
    {
        "name": "George Frideric Handel",
        "track_titles": [
            "Le Messie, HWV 56: Hallelujah Chorus"
        ]
    },
    {
        "name": "Gabriel Fauré",
        "track_titles": [
            "Pavane, Op. 50"
        ]
    },
    {
        "name": "Stanley Myers",
        "track_titles": [
            "Cavatina"
        ]
    },
    {
        "name": "Arcangelo Corelli,",
        "track_titles": [
            "Concerto Grosso No. 8 en Sol Mineur, Op. 6, \"Concerto de Noël\": Allegro"
        ]
    },
    {
        "name": "Sergueï Rachmaninov",
        "track_titles": [
            "Vocalise, Op. 34"
        ]
    },
    {
        "name": "Gustav Mahler",
        "track_titles": [
            "Symphonie No. 5: Adagietto"
        ]
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

    def find_composer(track_title):
        try:
            track_title = str(track_title)
        except ValueError:
            return None
        
        for composer in COMPOSERS_TRACKS:
            if track_title in composer["track_titles"]:
                print(f"[DEBUG] Match found: Track {track_title} -> Composer {composer['name']}")
                return composer["name"]
            
        print(f"[DEBUG] No composer match for track_id: {track_title}")
        return None

    quizz = []
    for track in tracks:
        # Create question
        q = {
            "id": track["id"],
            "title": track["title"],
            "preview": track["preview"]
        }

        # Find and add composer
        composer_name = find_composer(track["title"])
        if composer_name:
            q["composer"] = composer_name
            
            # Add to list (only when composer found)
            quizz.append(q)
        quizz.append(q)
        
    random.shuffle(quizz)
    return JsonResponse(quizz, safe=False)
