from rest_framework import generics
from rest_framework.views import APIView

from .mixins import PollMixin


class PollListAPIView(PollMixin, generics.ListAPIView):
    pass
    # queryset = Poll.objects.all()
    # serializer_class = PollSerializer


class PollDetailAPIView(PollMixin, generics.RetrieveAPIView):
    lookup_field = 'id'
    # queryset = Poll.objects.all()
    # serializer_class = PollSerializer
