from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView

from django.urls import reverse, reverse_lazy

from django.db.models import Q

from .models import Question, Answer, Category

from .forms import AskQuestionForm

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
        context['latest_questions'] = Question.objects.order_by('-created_at')[:3].select_related('author', 'category')
        # context['categories'] = int(self.request.GET.get('c', 0))
        return context


class QuestionDetailView(DetailView):
    pk_url_kwarg = 'pk'
    template_name = 'questionHub/detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None) -> Model:
        return get_object_or_404(Question, pk=self.kwargs[self.pk_url_kwarg])


class AskQuestionFormView(FormView):
    form_class = AskQuestionForm
    model = Question
    context_object_name = 'create_form'
    fields = ['category', 'title', 'content', 'is_closed']
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form, **kwargs):
        form = AskQuestionForm(self.request.POST)  # <- remove this line
        if form.is_valid():
            question = form.save(commit=False)
            question.author = self.request.user
            question.save()
            return super().form_valid(form)