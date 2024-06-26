from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

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

        recently_viewed_questions = self.request.session.get('recent_questions', [])
        questions = Question.objects.filter(id__in=recently_viewed_questions).select_related('author', 'category').reverse()
        context['recently_viewed_questions'] = questions
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
        context['amount_answers'] = Answer.objects.count()

        string_obj_id = str(self.object.id)

        if 'recent_questions' in self.request.session:
            if string_obj_id in self.request.session['recent_questions']:
                self.request.session['recent_questions'].remove(string_obj_id)

            recently_viewed_questions = Question.objects.filter(id__in=self.request.session['recent_questions']).select_related('author', 'category').reverse()
            self.request.session['recent_questions'].insert(0, string_obj_id)

            if len(self.request.session['recent_questions']) > 4:
                self.request.session['recent_questions'].pop()

            context['recently_viewed_questions'] = recently_viewed_questions
        else:
            self.request.session['recent_questions'] = [string_obj_id]
        
        self.request.session.modified = True
        return context


class AskQuestionView(LoginRequiredMixin, QuestionSingleObjectMixin, CreateView):
    form_class = AskQuestionForm
    context_object_name = 'create_form'
    template_name = 'questionHub/ask_question.html'

    def get_success_url(self):
        # print(self.__dict__)
        # print(self.request.session.items())
        return reverse_lazy('questionHub:detail', kwargs={'id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerView(LoginRequiredMixin, View):
    def post(self, request, id):
        question = get_object_or_404(Question, id=id)
        form = AnswerQuestionForm(request.POST)

        if form.is_valid(): 
            content = form.cleaned_data['content']

            Answer.objects.create(
                question=question,
                author=request.user,
                content=content
            )
            
            messages.success(request, 'Your answer was sent successfully!')
        else:
            messages.error(request, 'There was an error with your submission.')

        return redirect('questionHub:detail', id=id)


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
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

    def get_success_url(self):
        return reverse_lazy('questionHub:detail', kwargs={'id': self.kwargs[self.pk_url_kwarg]})

    def form_valid(self, form):
        messages.success(self.request, 'Question was updated successfully')
        return super().form_valid(form)


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
