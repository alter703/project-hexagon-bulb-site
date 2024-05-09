from typing import Any
from django.shortcuts import render
from django.views.generic import ListView


from .models import Question, Answer, Category

# Create your views here.
# def index(request):
#     return render(request, 'questionHub/index.html')

class QuestionsListView(ListView):
    model = Question
    template_name = "questionHub/index.html"
    context_object_name = 'questions'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questions'] = Question.objects.order_by('-created_at')[:2]  # Отримати 5 останніх питань
        return context
