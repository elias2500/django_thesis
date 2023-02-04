from django import forms
from .models import Project, Riddle

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'max_players', 'has_actor', 'scenario']

class RiddleForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                      empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Project')

    class Meta:
        model = Riddle
        fields = ['project','description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()
        self.fields['project'].label_from_instance = lambda obj: obj.title

