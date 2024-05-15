from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, CreateView, View
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.db.models import Q

from .models import Question, Answer, Category

from .forms import AskQuestionForm, AnswerQuestionForm

# Create your views here.
class QuestionsListView(ListView):
    model = Question
    template_name = "questionHub/index.html"
    context_object_name = 'questions'
    paginate_by = 9

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
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Question.objects.select_related('author', 'author__profile').prefetch_related('answers__question', 'answers__author__profile')

    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerQuestionForm
        context['question_absolute_url'] = self.object.get_absolute_url()
        return context


class AskQuestionCreateView(CreateView):
    form_class = AskQuestionForm
    model = Question
    context_object_name = 'create_form'
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        # print(self.object)
        return reverse_lazy('questionHub:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class AnswerView(LoginRequiredMixin, View):
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        form = AnswerQuestionForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                question=question,
                author=request.user,
                content=form.cleaned_data['content']
            )
            answer.save()
        return redirect('questionHub:detail', slug=slug)
