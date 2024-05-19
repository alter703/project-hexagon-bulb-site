from django.views.generic import ListView, DetailView, CreateView, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PollForm, AnswerFormSet, AnswerForm
from .models import Poll

from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse, reverse_lazy


# Create your views here.
class PollsListView(ListView):
    model = Poll
    template_name = "pollFeed/index.html"
    context_object_name = 'polls'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author', 'category').prefetch_related('answers').filter(Q(is_closed=False)).order_by('?')
        return queryset


class CreatePollView(LoginRequiredMixin, View):
    def get(self, request):
        poll_form = PollForm()
        answer_forms = [AnswerForm(prefix=str(i)) for i in range(0, 5)]
        return render(request, 'pollFeed/create_poll.html', {'poll_form': poll_form, 'answer_forms': answer_forms})

    def post(self, request):
        poll_form = PollForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(0, 5)]
        if poll_form.is_valid() and all(answer_form.is_valid() for answer_form in answer_forms):
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.slug = slugify(unidecode(f'{poll.question.split(' ')[:10]} by {poll.author}'))
            poll.save()
            for answer_form in answer_forms:
                if answer_form.cleaned_data.get('content'):
                    answer = answer_form.save(commit=False)
                    print(answer == True)
                    answer.poll = poll
                    answer.save()
            return redirect('main:index')
        return render(request, 'pollFeed/create_poll.html', {'poll_form': poll_form, 'answer_forms': answer_forms})
