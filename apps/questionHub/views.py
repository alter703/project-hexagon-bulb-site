from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Question, Answer, Category
from .forms import AskQuestionForm, AnswerQuestionForm
from .mixins import QuestionMultipleObjectMixin, QuestionsByCategoryMixin, QuestionSingleObjectMixin


# Create your views here.
class QuestionsListView(QuestionMultipleObjectMixin, ListView):
    template_name = "questionHub/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questions'] = Question.objects.filter(is_closed=False).select_related('author', 'category')[:3]
        context['categories'] = Category.objects.all()
        return context


class QuestionsByCategoryListView(QuestionsByCategoryMixin, ListView):
    template_name = "questionHub/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = Category.objects.filter(id=self.kwargs.get('id')).values_list('name', flat=True).first() # flat is for passing in a single field only
        return context


class QuestionDetailView(QuestionSingleObjectMixin, DetailView):
    template_name = 'questionHub/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerQuestionForm
        context['other_questions'] = Question.objects.filter(category=self.object.category)[:3].select_related('author', 'category')
        context['amount_answers'] = Answer.objects.count()
        return context


class AskQuestionCreateView(LoginRequiredMixin, QuestionSingleObjectMixin, CreateView):
    form_class = AskQuestionForm
    context_object_name = 'create_form'
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        return reverse_lazy('questionHub:detail', kwargs={'id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        save_form = super().form_valid(form)
        return save_form


class AnswerView(LoginRequiredMixin, View):
    def post(self, request, id):
        question = get_object_or_404(Question, id=id)
        form = AnswerQuestionForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                question=question,
                author=request.user,
                content=form.cleaned_data['content']
            )
            answer.save()
        messages.success(request, 'Your answer was sent successfully!')
        return redirect('questionHub:detail', id=id)


class QuestionDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        question = get_object_or_404(Question, id=id, author=request.user)
        question.delete()
        messages.success(request, 'Question was deleted successfully')
        return redirect('questionHub:index')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = AskQuestionForm
    template_name = 'questionHub/edit_question.html'
    context_object_name = 'question'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Question was updated successfully')
        return reverse_lazy('questionHub:detail', kwargs={'id': self.kwargs[self.pk_url_kwarg]})

    def form_invalid(self, form):
        messages.error(self.request, 'Error while updating Question')
        return super().form_invalid(form)


class CloseQuestionView(LoginRequiredMixin, View):
    def post(self, request, id):
        question = get_object_or_404(Question, id=id)
        if question.author == request.user:
            question.is_closed = True
            question.save()
            messages.success(request, "Question has been closed. Check the results!")
        else:
            messages.error(request, "You do not have permission to close this question.")
        return redirect('questionHub:detail', id=id)

    def get(self, request, *args, **kwargs):
        return redirect('questionHub:detail', id=kwargs['id'])


class BookmarkView(View):
    def get(self, request, id):
        user_bookmark = None
        question = get_object_or_404(Question, id=id)

        if request.user in question.bookmarks.all():
            question.bookmarks.remove(request.user)
            user_bookmark = False
        else:
            question.bookmarks.add(request.user)
            user_bookmark = True

        return JsonResponse({'user_bookmark': user_bookmark})
