from apps.questionHub.models import Question, Category
from .serializers import QuestionSerializer, CategorySerializer


class QuestionMixin:
    def get_serializer_class(self):
        return QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()


class CategoryMixin:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

