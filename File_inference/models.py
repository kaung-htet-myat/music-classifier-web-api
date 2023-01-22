from django.db import models
from django.contrib.auth.models import User


class FileInferenceModel(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='file_inferences')
    file = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=50)
