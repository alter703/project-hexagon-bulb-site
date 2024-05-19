from django.db import IntegrityError

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.db.models import Q

from .models import Question, Answer, Category
from .forms import AskQuestionForm, AnswerQuestionForm

from unidecode import unidecode

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
        context['other_questions'] = Question.objects.filter(category=self.object.category)[:3].select_related('author', 'category')
        return context


class AskQuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = AskQuestionForm
    model = Question
    context_object_name = 'create_form'
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        return reverse_lazy('questionHub:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        # try:
            form.instance.author = self.request.user
            # slug_text = unidecode(f'{form.instance.title.split(' ')[:10]} by {form.instance.author}')  # Конвертуємо кириличний текст в ASCII
            # form.instance.slug = slugify(slug_text)
            save_form = super().form_valid(form)
        # except IntegrityError:
            # form.add_error(None, 'You cannot ask exactly this question because you did! Delete existing one or type another title.')
            # return self.form_invalid(form)
        # else:
            # messages.success(self.request, f"You've asked the question! Now wait for an answer...")
            return save_form

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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


class QuestionDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug, author=request.user)
        question.delete()
        messages.success(request, 'Post was deleted successfully')
        return redirect('questionHub:index')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = AskQuestionForm
    template_name = 'questionHub/edit_question.html'
    context_object_name = 'question'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Post was updated successfully')
        return reverse_lazy('questionHub:detail', kwargs={'slug': self.object.slug})

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating post')
        return super().form_invalid(form)

