from rest_framework import generics
from rest_framework.views import APIView

from .mixins import PollMixin


class PollListAPIView(PollMixin, generics.ListAPIView):
    pass


class PollDetailAPIView(PollMixin, generics.RetrieveAPIView):
    lookup_field = 'id'
