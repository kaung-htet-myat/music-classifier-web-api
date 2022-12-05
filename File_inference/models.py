from django.db import models


class FileInferenceModel(models.Model):
    file = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=50)
