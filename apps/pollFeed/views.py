from django.views.generic import ListView, DetailView, CreateView, FormView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse, reverse_lazy

from .models import Poll

from .forms import PollForm

# Create your views here.
class PollsListView(ListView):
    model = Poll
    template_name = "pollFeed/index.html"
    context_object_name = 'polls'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author', 'category').prefetch_related('answers').filter(Q(is_closed=False)).order_by('?')
        return queryset

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PollForm, AnswerFormSet, AnswerForm
from .models import Poll

@login_required
def create_poll_view(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(0, 5)]  # Ліміт на 5 відповідей, можна змінити на більше
        if poll_form.is_valid() and all(answer_form.is_valid() for answer_form in answer_forms):
            poll = poll_form.save(commit=False)
            for answer_form in answer_forms:
                if answer_form.cleaned_data.get('content'):  # Перевірка на наявність відповіді
                    answer = answer_form.save(commit=False)
                    answer.poll = poll
                    poll.author = request.user
                    poll.save()
                    answer.save()
            return redirect('main:index')
    else:
        poll_form = PollForm()
        answer_forms = [AnswerForm(prefix=str(i)) for i in range(0, 5)]

    return render(request, 'pollFeed/create_poll.html', {'poll_form': poll_form, 'answer_forms': answer_forms})
