from django.http import JsonResponse
from .models import  Instrument


def instruments_list(request):
    instruments = Instrument.objects.all().order_by('?')[:10].values()
    return JsonResponse(list(instruments), safe=False)