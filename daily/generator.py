from lessons.models import Lesson, CompletedLesson

GAMES = [
    {'type': 'notes_reading',  'title': 'Lecture de notes',         'minutes': 3, 'auto': True},
    {'type': 'blind_test',     'title': 'Blind test',               'minutes': 2, 'auto': False},
    {'type': 'scales_builder', 'title': 'Construction de gammes',   'minutes': 3, 'auto': False},
]


def generate_activities(profile, time_goal):
    """
    Returns a list of dicts describing the activities for a daily program.
    Alternates between games and lessons, filling up to time_goal minutes.
    """
    completed_ids = set(
        CompletedLesson.objects.filter(profile=profile, is_completed=True).values_list('lesson_id', flat=True)
    )
    next_lessons = list(
        Lesson.objects.exclude(id__in=completed_ids).order_by('order')
    )

    activities = []
    remaining = time_goal
    lesson_idx = 0
    game_idx = 0
    want_game = True  # alternate: start with game

    while remaining > 0:
        if want_game:
            game = GAMES[game_idx % len(GAMES)]
            if game['minutes'] <= remaining:
                activities.append({
                    'activity_type': game['type'],
                    'activity_ref': '',
                    'activity_title': game['title'],
                    'estimated_minutes': game['minutes'],
                })
                remaining -= game['minutes']
                game_idx += 1
                want_game = False
            else:
                break
        else:
            if lesson_idx < len(next_lessons):
                lesson = next_lessons[lesson_idx]
                if 5 <= remaining:
                    activities.append({
                        'activity_type': 'lesson',
                        'activity_ref': lesson.slug,
                        'activity_title': lesson.title,
                        'estimated_minutes': 5,
                    })
                    remaining -= 5
                    lesson_idx += 1
                    want_game = True
                else:
                    break
            else:
                # No more unread lessons — add another game
                game = GAMES[game_idx % len(GAMES)]
                if game['minutes'] <= remaining:
                    activities.append({
                        'activity_type': game['type'],
                        'activity_ref': '',
                        'activity_title': game['title'],
                        'estimated_minutes': game['minutes'],
                    })
                    remaining -= game['minutes']
                    game_idx += 1
                else:
                    break

    return activities
