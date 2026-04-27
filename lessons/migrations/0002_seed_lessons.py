from django.db import migrations


LESSONS = [
    (1,  "Écrire la musique",              "ecrire-la-musique",      "1",  1),
    (2,  "Le rythme et la mesure",          "rythme-et-mesure",       "2",  2),
    (3,  "Les clés musicales",              "cles-musicales",         "3",  3),
    (4,  "Les altérations",                 "alterations",            "4",  4),
    (5,  "Les intervalles",                 "intervalles",            "5",  5),
    (6,  "Les gammes majeures",             "gammes-majeures",        "6",  6),
    (7,  "Les gammes mineures",             "gammes-mineures",        "7",  7),
    (8,  "Les accords",                     "accords",                "8",  8),
    (9,  "Les nuances et le tempo",         "nuances-et-tempo",       "9",  9),
    (10, "La forme musicale",               "forme-musicale",         "10", 10),
    (11, "Les cadences",                    "cadences",               "11", 11),
    (12, "Les progressions d'accords",      "progressions-accords",   "12", 12),
    (13, "La ligne de basse",               "ligne-de-basse",         "13", 13),
    (14, "Les modes",                       "modes",                  "14", 14),
    (15, "La modulation",                   "modulation",             "15", 15),
    (16, "Les ornements",                   "ornements",              "16", 16),
    (17, "Les liaisons et articulations",   "liaisons-articulations", "17", 17),
    (18, "La lecture rythmique avancée",    "rythme-avance",          "18", 18),
    (19, "L'harmonisation d'une mélodie",   "harmonisation",          "19", 19),
    (20, "Le chiffrage des accords",        "chiffrage-accords",      "20", 20),
    (21, "Introduction au contrepoint",     "contrepoint",            "21", 21),
    (22, "Analyse musicale — niveau 1",     "analyse-musicale",       "22", 22),
    (23, "La fugue",                        "fugue",                  "23", 23),
    (24, "L'harmonie jazz",                 "harmonie-jazz",          "24", 24),
    (25, "La composition",                  "composition",            "25", 25),
    (26, "L'improvisation",                 "improvisation",          "26", 26),
    (27, "L'orchestration",                 "orchestration",          "27", 27),
    (28, "La musique contemporaine",        "musique-contemporaine",  "28", 28),
]


def seed_lessons(apps, schema_editor):
    Lesson = apps.get_model("lessons", "Lesson")
    for pk, title, slug, chapter, order in LESSONS:
        Lesson.objects.update_or_create(
            slug=slug,
            defaults={"id": pk, "title": title, "chapter": chapter, "order": order},
        )


def unseed_lessons(apps, schema_editor):
    Lesson = apps.get_model("lessons", "Lesson")
    slugs = [row[2] for row in LESSONS]
    Lesson.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_lessons, reverse_code=unseed_lessons),
    ]
