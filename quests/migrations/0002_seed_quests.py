from django.db import migrations

QUESTS = [
    # (title, description, quest_type, required_count, xp_reward, keys_reward, order)
    ("Premier pas",         "Lis ton premier cours",                          "read_lesson",        1,  15,  3,  1),
    ("Explorateur",         "Lis 5 cours",                                    "read_lesson",        5,  30,  8,  2),
    ("Débutant accompli",   "Complète les 10 premiers cours",                 "read_lesson",        10, 60,  15, 3),
    ("Studieux",            "Lis 20 cours",                                   "read_lesson",        20, 100, 25, 4),
    ("Maître du solfège",   "Lis les 28 cours — félicitations !",             "read_lesson",        28, 200, 50, 5),
    ("Première partie",     "Fais une partie de lecture de notes",            "play_notes_reading", 1,  10,  2,  6),
    ("Lecteur de notes",    "Fais 5 parties de lecture de notes",             "play_notes_reading", 5,  25,  6,  7),
    ("Champion de notes",   "Fais 20 parties de lecture de notes",            "play_notes_reading", 20, 60,  15, 8),
]


def seed_quests(apps, schema_editor):
    Quest = apps.get_model("quests", "Quest")
    for title, description, quest_type, required_count, xp_reward, keys_reward, order in QUESTS:
        Quest.objects.update_or_create(
            title=title,
            defaults={
                "description": description,
                "quest_type": quest_type,
                "required_count": required_count,
                "xp_reward": xp_reward,
                "keys_reward": keys_reward,
                "order": order,
            },
        )


def unseed_quests(apps, schema_editor):
    Quest = apps.get_model("quests", "Quest")
    Quest.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_quests, reverse_code=unseed_quests),
    ]
