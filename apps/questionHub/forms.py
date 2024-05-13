from django.forms import ModelForm
from .models import Question 


class AskQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content', 'category')
