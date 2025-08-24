from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Lesson, Profile, CompletedLesson
from django.utils import timezone


def get_completed_ids(profile):
    return set(
        CompletedLesson.objects.filter(profile=profile, is_completed=True).values_list("lesson_id", flat=True)
    )


def lessons_list(request):
    lessons = Lesson.objects.all().order_by('order')
    completed_ids = []
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        completed_ids = get_completed_ids(profile)
    data = [
        {
            "id": lesson.id,
            "title": lesson.title,
            "slug": lesson.slug,
            "chapter": lesson.chapter,
            "order": lesson.order,
            "completed": lesson.id in completed_ids
        }
        for lesson in lessons
    ] 
    return JsonResponse(data, safe=False)


def lesson(request, lesson_slug):
    profile = get_object_or_404(Profile, user=request.user)
    completed_ids = get_completed_ids(profile)
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    data = model_to_dict(lesson, fields=['id', 'title', 'slug', 'chapter', 'order'])
    data["completed"] = lesson.id in completed_ids
    return JsonResponse(data, safe=False)


def complete_lesson(request, lesson_slug):
    profile = get_object_or_404(Profile, user=request.user)
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    message = ""
    
    completed, created = CompletedLesson.objects.get_or_create(profile=profile, lesson=lesson)
    
    if not completed.is_completed:
        completed.is_completed = True
        completed.completed_at = timezone.now().date()
        completed.save()
        
        if created: # reward only on first completion
            profile.experience += 10
            profile.add_keys(5)
            profile.save()
            message = "Lesson completed! Rewards granted."
        else:
            message = "Lesson already completed"
            
    return JsonResponse({
        "message": message, 
        "lesson_id": lesson.id, 
        "completed": True, 
        "updated_xp": profile.experience, 
        "level": profile.get_level(), 
        "progress": round(profile.get_progression_ratio(), 2)
    })


def uncomplete_lesson(request, lesson_slug):
    profile = get_object_or_404(Profile, user=request.user)
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    
    completed_lesson = get_object_or_404(CompletedLesson, profile=profile, lesson=lesson)
    completed_lesson.is_completed = False
    completed_lesson.save()
    
    return JsonResponse({'message': 'Lesson has been marked has unfinished', 'lesson_id': lesson.id})
    