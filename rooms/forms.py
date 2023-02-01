from django import forms
from . import models

class RoomForm(forms.ModelForm):
    class Meta:
        fields = ('title','noOfPlayers','difficulty','hasActor','theme','scenario')
        model = models.Room

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)