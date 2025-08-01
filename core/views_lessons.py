from django.http import JsonResponse
from .models import Lesson

def lessons_list(request):
    lessons = Lesson.objects.all().order_by('-order')
    data = [
        {
            "title": lesson.title,
            "slug": lesson.slug,
            "chapter": lesson.chapter,
            "order": lesson.order
        }
        for lesson in lessons
    ] 
    return JsonResponse(data, safe=False)