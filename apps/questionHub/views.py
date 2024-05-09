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
