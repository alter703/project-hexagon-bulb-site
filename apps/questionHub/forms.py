from django import forms
from .models import Question, Category


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'category', 'content',)
        widgets = {
            'category': forms.RadioSelect,
        }