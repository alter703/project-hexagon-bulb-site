from rest_framework import generics
from apps.pollFeed.models import Poll
from .serializers import PollSerializer

class PollMixin:
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
