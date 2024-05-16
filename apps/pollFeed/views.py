from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Poll

# Create your views here.
class PollsListView(ListView):
    model = Poll
    template_name = "pollFeed/index.html"
    context_object_name = 'polls'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author', 'category').filter(Q(is_closed=False)).order_by('?')
        return queryset
