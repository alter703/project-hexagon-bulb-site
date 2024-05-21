from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
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
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            queryset = Question.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).select_related('author', 'category')
        else:
            queryset = Question.objects.filter(Q(is_closed=False)).select_related('author', 'category').order_by('?')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questions'] = Question.objects.filter(is_closed=False).select_related('author', 'category')[:3]
        context['query'] = self.request.GET.get('q', '')
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
        context['amount_answers'] = Answer.objects.count()
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
        form.instance.author = self.request.user
        save_form = super().form_valid(form)
        return save_form


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
        messages.success(request, 'Question was deleted successfully')
        return redirect('questionHub:index')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = AskQuestionForm
    template_name = 'questionHub/edit_question.html'
    context_object_name = 'question'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Question was updated successfully')
        return reverse_lazy('questionHub:detail', kwargs={'slug': self.object.slug})

    def form_invalid(self, form):
        messages.error(self.request, 'Error while updating Question')
        return super().form_invalid(form)


class CloseQuestionView(LoginRequiredMixin, View):
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        if question.author == request.user:
            question.is_closed = True
            question.save()
            messages.success(request, "Question has been closed. Check the results!")
        else:
            messages.error(request, "You do not have permission to close this question.")
        return redirect('questionHub:detail', slug=slug)

    def get(self, request, *args, **kwargs):
        return redirect('questionHub:detail', slug=kwargs['slug'])


class BookmarkView(View):
    def get(self, request, slug):
        user_bookmark = None
        question = get_object_or_404(Question, slug=slug)

        if request.user in question.bookmarks.all():
            question.bookmarks.remove(request.user)
            user_bookmark = False
        else:
            question.bookmarks.add(request.user)
            user_bookmark = True

        return JsonResponse({'user_bookmark': user_bookmark})