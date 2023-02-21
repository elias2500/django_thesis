from django import forms
from .models import Project, Riddle

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'max_players', 'has_actor', 'scenario']


class RiddleForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=None,
                                      empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Project')

    class Meta:
        model = Riddle
        fields = ['project', 'description']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = request.user.rooms.all()
        self.fields['project'].label_from_instance = lambda obj: obj.title

    def save(self, commit=True):
        riddle = super().save(commit=False)
        riddle.project = self.cleaned_data['project']
        if commit:
            riddle.save()
        return riddle
