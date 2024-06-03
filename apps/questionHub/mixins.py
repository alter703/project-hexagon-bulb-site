from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin

from apps.questionHub.models import Category, Question


class QuestionMultipleObjectMixin(MultipleObjectMixin):
    model = Question
    paginate_by = 6
    context_object_name = 'questions'

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if query:
            if query.startswith('#'):
                queryset = Question.objects.filter(Q(category__name__icontains=query[1:])).select_related('author', 'category').prefetch_related('answers')
            else:
                queryset = Question.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).select_related('author', 'category').prefetch_related('answers')
        else:
            queryset = Question.objects.filter(Q(is_closed=False)).select_related('author', 'category').order_by('?').prefetch_related('answers')
        return queryset

class QuestionsByCategoryMixin(QuestionMultipleObjectMixin):
    # model = Question
    # template_name = "questionHub/category_list.html"
    context_object_name = 'cat_questions'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs.get('id')
        category = get_object_or_404(Category, id=category_id)
        queryset = Question.objects.filter(category=category).select_related('author', 'category').prefetch_related('answers')
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = get_object_or_404(Category, id=self.kwargs.get('id'))
    #     return context

class QuestionSingleObjectMixin(SingleObjectMixin):
    model = Question
    context_object_name = 'question'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Question.objects.select_related('author', 'author__profile').prefetch_related('answers__question', 'answers__author__profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), id=self.kwargs[self.pk_url_kwarg])
