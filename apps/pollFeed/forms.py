from django import forms

from .models import Poll, Answer

AnswerFormSet = forms.inlineformset_factory(
    Poll,  
    Answer,  
    fields=('content', 'is_correct'),  
    extra=1,  
    can_delete=True,  
)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'is_correct']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question', 'category')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["category"].required = True
