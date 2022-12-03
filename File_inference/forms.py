from django import forms

class UploadFileForm(forms.Form):
    song_file = forms.FileField()