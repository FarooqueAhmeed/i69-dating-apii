from celery import shared_task
from django.core.files import File
from pathlib import Path
from django.core.files.storage import default_storage
from .models import Story
import tempfile
import cv2
import os
from django.core.files.base import ContentFile


@shared_task(name="clear_story")
def clean_story(*args, **kwargs):
    from moments.models import Story
    import datetime

    if args:
        hours = int(args[0])
    else:
        hours = 1
    timedelta = datetime.timedelta(hours)
    Story.objects.filter(created_date__gte=datetime.datetime.now() - timedelta).delete()


@shared_task
def createThumbnail(id):
    story = Story.objects.get(id=id)
    with tempfile.NamedTemporaryFile(mode="wb") as vid:
        vidcap = cv2.VideoCapture(story.file.path)

        success, image = vidcap.read()

        if success:
            _, img = cv2.imencode(".jpeg", image)
            img.tobytes()
            file = ContentFile(img)
            story.thumbnail.save(
                os.path.basename(story.thumbnail.name), file, save=True
            )
            return


@shared_task
def broadcast_story_type(story_ids):
    from moments.schema import OnUpdateStory

    for story_id in story_ids:
        OnUpdateStory.broadcast(group=None, payload={"story_id": story_id})
        import time

        time.sleep(1)
    return
