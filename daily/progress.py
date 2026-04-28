from django.utils import timezone
from .models import DailyProgram, DailyActivity


def complete_daily_activity(profile, activity_type, activity_ref=''):
    """
    Called after a user completes an action (lesson or game session).
    Marks the first matching uncompleted activity in today's program as done.
    """
    today = timezone.now().date()
    try:
        program = DailyProgram.objects.get(profile=profile, date=today)
    except DailyProgram.DoesNotExist:
        return

    activity = program.activities.filter(
        activity_type=activity_type,
        completed=False,
        **(({'activity_ref': activity_ref}) if activity_ref else {})
    ).first()

    if activity:
        activity.completed = True
        activity.completed_at = timezone.now()
        activity.save()
