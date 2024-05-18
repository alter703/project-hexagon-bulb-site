from django import forms
from .models import Poll, Choice

PollFormSet = forms.inlineformset_factory(
    Poll,  
    Choice,  
    fields=('text',),  
    extra=1,  
    can_delete=True,  
)

pollformset = PollFormSet()


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
