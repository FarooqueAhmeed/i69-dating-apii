from django.urls import path
from . import views

urlpatterns = [
    path("", views.returnSounds, name="return_sounds"),
]
