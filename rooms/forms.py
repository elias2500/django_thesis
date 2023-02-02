from django import forms
from .models import Project, Riddle

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'max_players', 'has_actor', 'scenario']

class RiddleForm(forms.ModelForm):
    class Meta:
        model = Riddle
        fields = ['description']
