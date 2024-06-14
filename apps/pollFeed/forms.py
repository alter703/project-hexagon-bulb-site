from django import forms
from .models import Poll, Choice


class CreatePollForm(forms.ModelForm):
    choice1 = forms.CharField(max_length=255, label='Choice 1')
    choice2 = forms.CharField(max_length=255, label='Choice 2')
    choice3 = forms.CharField(max_length=255, label='Choice 3')
    choice4 = forms.CharField(max_length=255, label='Choice 4')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for index in range(1, 5):
            self.fields[f"choice{index}"].required = False

    class Meta:
        model = Poll
        fields = ('text',)

    def save(self, commit=True):
        poll = super().save(commit=commit)

        choice1 = Choice(poll=poll, text=self.cleaned_data['choice1'])
        choice2 = Choice(poll=poll, text=self.cleaned_data['choice2'])
        choice3 = Choice(poll=poll, text=self.cleaned_data['choice3'])
        choice4 = Choice(poll=poll, text=self.cleaned_data['choice4'])

        if commit:
            list_choices = [choice1, choice2, choice3, choice4]

            for choice in list_choices:
                choice.save()

            poll.save()

        return poll
