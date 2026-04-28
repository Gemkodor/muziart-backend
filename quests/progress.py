from .models import Quest, UserQuest


def check_quest_progress(profile, quest_type):
    """
    Called after a user action. Increments progress on all matching quests
    that are not yet claimed. Returns list of newly completed quest IDs.
    """
    quests = Quest.objects.filter(quest_type=quest_type)
    newly_completed = []

    for quest in quests:
        user_quest, _ = UserQuest.objects.get_or_create(profile=profile, quest=quest)
        if user_quest.claimed:
            continue
        if user_quest.progress < quest.required_count:
            user_quest.progress += 1
            user_quest.save()
            if user_quest.progress >= quest.required_count:
                newly_completed.append(quest.id)

    return newly_completed
