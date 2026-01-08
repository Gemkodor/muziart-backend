from django.http import JsonResponse
from .models import  Instrument


def instruments_list(request):
    instruments = Instrument.objects.all().order_by('?').values()
    return JsonResponse(list(instruments), safe=False)