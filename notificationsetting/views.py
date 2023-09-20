from django.http import JsonResponse
from django.shortcuts import render
from .models import NotificationSound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def returnSounds(request):
    sounds = NotificationSound.objects.all()
    sound_dict = {}
    for sound in sounds:
        sound_dict[sound.name] = sound.file.name

    return JsonResponse(sound_dict)
