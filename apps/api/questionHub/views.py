from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.questionHub.serializers import QuestionSerializer
from django.contrib.auth.models import User
from apps.questionHub.models import Category, Question

@api_view(['GET', ])
def question_detail(request, id):
    # print(request.data)
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


# @api_view(['POST', ])
# def question_post(request):
#     # request.data['category'] = Category.objects.get(id=request.data['category']).id
#     request.data['author'] = User.objects.get(id=1).id
#     print(request.data['category'])
#     serializer = QuestionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)