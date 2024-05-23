from django.shortcuts import render
from apps.questionHub.models import Question
# Create your views here.
def index(request):

    context = {
        'questions': Question.objects.filter(is_closed=False).order_by('?')[:4].select_related('author', 'category').prefetch_related('answers')
    }

    return render(request, 'main/index.html', context)

def whats_new_view(request):
    return render(request, 'main/whats_new.html')

def error_404_view(request, exception):
    return render(request, 'main/error_404.html')

def about_view(request):
    return render(request, 'main/about_us.html')