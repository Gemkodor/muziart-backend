"""
Management command: populate_instruments

Resets the Instrument and InstrumentCategory tables, then fetches
a representative Wikimedia Commons image for each instrument via the
Commons API.

Usage:
    python manage.py populate_instruments
    python manage.py populate_instruments --dry-run   # print URLs without saving
"""
import time
import urllib.request
import urllib.parse
import json

from django.core.management.base import BaseCommand

from games.models import Instrument, InstrumentCategory

# ---------------------------------------------------------------------------
# Master instrument list
# Format: (french_name, search_term_for_wikimedia, local_image_name_or_empty)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "Cordes frottées": [
        ("Violon",       "violin musical instrument",           "violon.jpg"),
        ("Alto",         "viola musical instrument",            "alto.jpg"),
        ("Violoncelle",  "cello musical instrument",            "violoncelle.jpeg"),
        ("Contrebasse",  "double bass musical instrument",      "contrebasse.jpg"),
    ],
    "Cordes pincées": [
        ("Guitare classique", "classical guitar instrument",   "guitare.jpg"),
        ("Harpe",         "concert harp instrument",           "harpe.jpg"),
        ("Luth",          "lute instrument",                   "luth.jpg"),
        ("Mandoline",     "mandolin instrument",               "mandoline.jpg"),
        ("Banjo",         "banjo instrument",                  "banjo.jpg"),
        ("Balalaïka",     "balalaika instrument",              "balalaika.jpg"),
    ],
    "Cordes frappées": [
        ("Piano",         "grand piano instrument",            "piano.jpg"),
        ("Clavecin",      "harpsichord instrument",            "clavecin.jpg"),
        ("Célesta",       "celesta instrument",                "celesta.jpg"),
    ],
    "Bois": [
        ("Flûte traversière", "concert flute instrument",     "flute_traversiere.jpg"),
        ("Flûte à bec",   "recorder instrument",              "flute_a_bec.jpg"),
        ("Hautbois",      "oboe instrument",                  "hautbois.jpg"),
        ("Cor anglais",   "cor anglais instrument",           "cor_anglais.jpg"),
        ("Clarinette",    "clarinet instrument",              "clarinette.jpg"),
        ("Clarinette basse", "bass clarinet instrument",      "clarinette_basse.jpg"),
        ("Basson",        "bassoon instrument",               "basson_moderne.jpg"),
        ("Contrebasson",  "contrabassoon instrument",         "contrebasson.jpg"),
        ("Saxophone",     "saxophone instrument",             "saxophone.jpg"),
    ],
    "Cuivres": [
        ("Trompette",     "trumpet instrument",               "trompette.jpg"),
        ("Cor d'harmonie", "french horn instrument",          "cor_harmonie.jpg"),
        ("Trombone",      "trombone instrument",              "trombone.jpg"),
        ("Tuba",          "tuba instrument",                  "tuba.jpg"),
        ("Bugle",         "bugle instrument",                 "bugle.jpg"),
        ("Euphonium",     "euphonium instrument",             "euphonium.jpg"),
    ],
    "Percussions": [
        ("Timbale",       "timpani instrument",               "timbale.jpg"),
        ("Caisse claire", "snare drum instrument",            "caisse_claire.jpg"),
        ("Grosse caisse", "bass drum instrument",             "grosse_caisse.jpg"),
        ("Xylophone",     "xylophone instrument",             "xylophone.jpg"),
        ("Marimba",       "marimba instrument",               "marimba.jpg"),
        ("Vibraphone",    "vibraphone instrument",            "vibraphone.jpg"),
        ("Glockenspiel",  "glockenspiel instrument",          "glockenspiel.jpg"),
        ("Triangle",      "triangle percussion instrument",   "triangle.jpg"),
        ("Cymbale",       "cymbal instrument",                "cymbale.jpg"),
        ("Tambourin",     "tambourine instrument",            "tambourin.jpg"),
    ],
    "Claviers": [
        ("Orgue",         "pipe organ instrument",            "orgue.JPG"),
        ("Accordéon",     "accordion instrument",             "accordion.jpg"),
        ("Synthétiseur",  "synthesizer keyboard instrument",  "synthetiseur.jpg"),
        ("Clavicorde",    "clavichord instrument",            ""),
    ],
}

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "MuziartBot/1.0 (music education app; contact: gemkodor@gmail.com)"


def _wikimedia_get(params: dict) -> dict:
    query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"{WIKIMEDIA_API}?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception:
        return {}


def _search_image(search_term: str) -> str:
    """Return the best Wikimedia Commons image URL for search_term, or ''."""
    # Step 1 — find a relevant file via fulltext search in File namespace
    data = _wikimedia_get({
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": "6",
        "srlimit": "5",
        "format": "json",
    })

    results = data.get("query", {}).get("search", [])
    if not results:
        return ""

    # Take the first result whose title looks like a photo (jpg/png/jpeg)
    file_title = ""
    for r in results:
        title = r["title"]
        if any(title.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
            file_title = title
            break

    if not file_title:
        return ""

    # Step 2 — get a 640px thumbnail URL for that file
    data2 = _wikimedia_get({
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": "640",
        "format": "json",
    })

    pages = data2.get("query", {}).get("pages", {})
    for page in pages.values():
        info = page.get("imageinfo", [])
        if info:
            return info[0].get("thumburl", "")

    return ""


class Command(BaseCommand):
    help = "Populate instruments and categories, fetching Wikimedia images."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Print results without saving.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if not dry_run:
            self.stdout.write("Clearing existing instruments and categories…")
            Instrument.objects.all().delete()
            InstrumentCategory.objects.all().delete()

        for cat_name, instruments in CATEGORIES.items():
            if dry_run:
                category = None
            else:
                category, _ = InstrumentCategory.objects.get_or_create(name=cat_name)

            self.stdout.write(f"\n-- {cat_name}")

            for (name, search_term, local_img) in instruments:
                self.stdout.write(f"   {name}… ", ending="")
                self.stdout.flush()

                image_url = _search_image(search_term)

                if image_url:
                    self.stdout.write(self.style.SUCCESS(f"OK  {image_url[:80]}"))
                else:
                    self.stdout.write(self.style.WARNING("no image found"))

                if not dry_run:
                    Instrument.objects.create(
                        name=name,
                        image_name=local_img,
                        image_url=image_url,
                        category=category,
                    )

                time.sleep(0.3)  # be polite to Wikimedia API

        self.stdout.write(self.style.SUCCESS("\nDone."))
