# Create your views here.
from django.http import HttpResponse
from watertank.models import WaterTankController


def index(request):

    wtc = WaterTankController.objects.get()

    
    msg = ''
    msg += wtc.pumpIsOn

    return HttpResponse(msg)
