from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin

from apps.pollFeed.models import Poll


class PollMultipleObjectMixin(MultipleObjectMixin):
    model = Poll
    paginate_by = 6
    context_object_name = 'polls'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Poll.objects.filter(is_closed=False).select_related('author').prefetch_related('choices')
        
        if query:
            queryset = queryset.filter(text__icontains=query)
        
        return queryset


class PollSingleObjectMixin(SingleObjectMixin):
    model = Poll
    context_object_name = 'poll'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Poll.objects.select_related('author', 'author__profile')

    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['id'])
