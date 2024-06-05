from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.questionHub.serializers import QuestionSerializer, CategorySerializer
from django.contrib.auth.models import User
from apps.questionHub.models import Category, Question
from rest_framework import generics
from rest_framework.views import APIView

from .mixins import QuestionMixin, CategoryMixin

class QuestionDetailAPIView(QuestionMixin, generics.RetrieveAPIView):
    lookup_field = 'id' 


class QuestionRandomAPIView(APIView):
    def get(self, request):
        try:
            question = Question.objects.order_by('?').first()
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


# @api_view(['GET', ])
# def question_random(request):
#     try:
#         question = Question.objects.order_by('?').first()
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)


class QuestionAPIView(APIView):
    def get(self, request):
        questions = Question.objects.values()
        return Response({'questions': questions, 'is_user_authenticated': request.user.is_authenticated})


class QuestionManageAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.data['author'] = request.user.id
        else:
            return Response({"AuthorizationError": "You are not authorized user to create Question."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'question': serializer.data})

    def put(self, request, *args, **kwargs):
        q_id = kwargs.get('id', None)

        if not q_id:
            return Response({'error': 'Method "PUT" is not allowed without an id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Question.objects.get(id=q_id)
        except Question.DoesNotExist:
            return Response({'error': 'This Question does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if instance.author != request.user:
            return Response({'AuthorError': 'You are not the author of this Question to update.'}, status=status.HTTP_403_FORBIDDEN)

        request.data['author'] = request.user.id
        serializer = QuestionSerializer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'question': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        q_id = kwargs.get('id', None)

        if not q_id:
            return Response({'error': 'Method "DELETE" is not allowed without an id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Question.objects.get(id=q_id)
        except Question.DoesNotExist:
            return Response({"error": "This Question does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if instance.author != request.user:
            return Response({'AuthorError': 'You are not the author of this Question to delete.'}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response({"success": "This Question is deleted."}, status=status.HTTP_200_OK)


class CategoryListAPIView(CategoryMixin, generics.ListAPIView):
    pass
