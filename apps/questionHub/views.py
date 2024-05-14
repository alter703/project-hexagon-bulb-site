from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.utils.text import slugify

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
        return context


class QuestionDetailView(DetailView):
    template_name = 'questionHub/detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None) -> Model:
        return get_object_or_404(Question, slug=self.kwargs[self.slug_url_kwarg])


class AskQuestionCreateView(CreateView):
    model = Question
    slug_url_kwarg = 'slug'
    context_object_name = 'create_form'
    fields = ['title', 'category', 'content']
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        # print(self.object)

        return reverse('questionHub:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)  # Генерація слагу з заголовка
        return super().form_valid(form)
