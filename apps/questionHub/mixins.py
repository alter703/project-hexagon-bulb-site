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
        queryset = Question.objects.select_related('author', 'category').prefetch_related('answers')

        if query:
            if query.startswith('#'):
                category_name = query[1:]
                queryset = queryset.filter(category__name__icontains=category_name)
            else:
                queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            queryset = queryset.filter(is_closed=False).order_by('?')

        return queryset


class QuestionsByCategoryMixin(QuestionMultipleObjectMixin):
    paginate_by = 9
    context_object_name = 'cat_questions'

    def get_queryset(self):
        category_id = self.kwargs.get('id')
        category = get_object_or_404(Category, id=category_id)
        queryset = Question.objects.filter(category=category).select_related('author', 'category').prefetch_related('answers')
        return queryset


class QuestionSingleObjectMixin(SingleObjectMixin):
    model = Question
    context_object_name = 'question'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Question.objects.select_related('author', 'author__profile').prefetch_related('answers__question', 'answers__author__profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), id=self.kwargs[self.pk_url_kwarg])
