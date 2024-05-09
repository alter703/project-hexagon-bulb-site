from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from django.db.models import Q

from .models import Question, Answer, Category

# Create your views here.
class QuestionsListView(ListView):
    model = Question
    template_name = "questionHub/index.html"
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author', 'category').filter(Q(is_closed=False)).order_by('?')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questions'] = Question.objects.order_by('-created_at')[:3]
        # context['categories'] = int(self.request.GET.get('c', 0))
        return context


class QuestionDetailView(DetailView):
    pk_url_kwarg = 'pk'
    template_name = 'questionHub/detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None) -> Model:
        return get_object_or_404(Question, pk=self.kwargs[self.pk_url_kwarg])
