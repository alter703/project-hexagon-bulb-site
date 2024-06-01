from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.questionHub.serializers import QuestionSerializer

from apps.questionHub.models import Question

@api_view(['GET', ])
def question_detail(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
