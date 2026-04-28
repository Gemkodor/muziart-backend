import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from core.models import Profile
from .models import DailyProgram, DailyActivity
from .generator import generate_activities, GAMES


def serialize_program(program):
    return {
        'id': program.id,
        'date': str(program.date),
        'time_goal': program.time_goal,
        'done_count': program.done_count,
        'total_count': program.total_count,
        'completed': program.completed,
        'activities': [
            {
                'id': a.id,
                'activity_type': a.activity_type,
                'activity_ref': a.activity_ref,
                'activity_title': a.activity_title,
                'estimated_minutes': a.estimated_minutes,
                'order': a.order,
                'completed': a.completed,
            }
            for a in program.activities.all()
        ],
    }


def today_program(request):
    profile = get_object_or_404(Profile, user=request.user)
    today = timezone.now().date()

    if request.method == 'GET':
        try:
            program = DailyProgram.objects.get(profile=profile, date=today)
            return JsonResponse(serialize_program(program))
        except DailyProgram.DoesNotExist:
            return JsonResponse({'exists': False})

    if request.method == 'POST':
        data = json.loads(request.body)
        time_goal = int(data.get('time_goal', 10))
        time_goal = max(5, min(time_goal, 60))

        # Delete existing program for today if regenerating
        DailyProgram.objects.filter(profile=profile, date=today).delete()

        program = DailyProgram.objects.create(profile=profile, date=today, time_goal=time_goal)

        for order, activity_data in enumerate(generate_activities(profile, time_goal)):
            DailyActivity.objects.create(program=program, order=order, **activity_data)

        return JsonResponse(serialize_program(program))

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def complete_activity(request, activity_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    profile = get_object_or_404(Profile, user=request.user)
    activity = get_object_or_404(DailyActivity, id=activity_id, program__profile=profile)

    if not activity.completed:
        activity.completed = True
        activity.completed_at = timezone.now()
        activity.save()

    return JsonResponse(serialize_program(activity.program))


def add_extra_activity(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    profile = get_object_or_404(Profile, user=request.user)
    today = timezone.now().date()
    program = get_object_or_404(DailyProgram, profile=profile, date=today)

    # Alternate between lesson and game, pick what wasn't the last activity
    last = program.activities.last()
    last_type = last.activity_type if last else None

    if last_type == 'lesson' or last_type is None:
        # Add a game not already in the program
        used_game_types = set(
            program.activities.filter(activity_type__in=[g['type'] for g in GAMES])
            .values_list('activity_type', flat=True)
        )
        game = next((g for g in GAMES if g['type'] not in used_game_types), GAMES[0])
        extra = DailyActivity.objects.create(
            program=program,
            activity_type=game['type'],
            activity_ref='',
            activity_title=game['title'],
            estimated_minutes=game['minutes'],
            order=program.total_count,
        )
    else:
        # Add next unread lesson
        from lessons.models import Lesson, CompletedLesson
        completed_ids = set(
            CompletedLesson.objects.filter(profile=profile, is_completed=True).values_list('lesson_id', flat=True)
        )
        used_slugs = set(program.activities.filter(activity_type='lesson').values_list('activity_ref', flat=True))
        lesson = (
            Lesson.objects.exclude(id__in=completed_ids).exclude(slug__in=used_slugs).order_by('order').first()
        )
        if not lesson:
            return JsonResponse({'error': 'No more lessons available'}, status=400)
        extra = DailyActivity.objects.create(
            program=program,
            activity_type='lesson',
            activity_ref=lesson.slug,
            activity_title=lesson.title,
            estimated_minutes=5,
            order=program.total_count,
        )

    return JsonResponse(serialize_program(program))
