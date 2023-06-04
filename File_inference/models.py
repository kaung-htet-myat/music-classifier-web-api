from django.db import models
from django.contrib.auth.models import User
from music_classifier_web_api.storage_backends import PublicMediaStorage


class FileInferenceModel(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='file_inferences')
    filename = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(storage=PublicMediaStorage)
    timestamp = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=50)