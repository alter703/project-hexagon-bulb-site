from django import forms
from .models import Poll, Choice


class CreatePollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('text',)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('text',)

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, ** kwargs)
        self.fields["text"].required = False
