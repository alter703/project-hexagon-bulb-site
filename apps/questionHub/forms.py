from django import forms
from .models import Question, Category, Answer


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'category', 'content',)
        widgets = {
            'category': forms.RadioSelect,
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["category"].required = True


class AnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
