from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.pollFeed.models import Poll
from .forms import CreatePollForm, ChoiceForm

# Create your views here.
class PollListView(ListView):
    model = Poll
    template_name = "pollFeed/index.html"
    context_object_name = 'polls'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author').order_by('?')
        return queryset


def create_poll(request):
    if request.method == "POST":
        poll_form = CreatePollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, request.FILES, prefix=str(i)) for i in range(0, 5)]
        if poll_form.is_valid() and all(answer_form.is_valid() for answer_form in choice_forms):
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()
            valid_answers = [answer_form for answer_form in choice_forms if answer_form.cleaned_data.get('text')]
            if len(valid_answers) < 2:
                messages.error(request, "You must type at least two choices!")
                return redirect('pollFeed:create')
            for answer_form in choice_forms:
                if answer_form.cleaned_data.get('text'):
                    answer = answer_form.save(commit=False)
                    answer.poll = poll
                    answer.author = request.user
                    answer.save()
            return redirect('pollFeed:index')
    else:
        poll_form = CreatePollForm()
        answer_forms = [ChoiceForm(prefix=str(i)) for i in range(0, 5)]
    return render(request, "pollFeed/create_poll.html", {"answer_forms": answer_forms, "poll_form": poll_form})
