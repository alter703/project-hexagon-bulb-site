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


class QuestionAskAPIView(APIView):
    def post(self, request):
        request.data['author'] = request.user.id

        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'question': serializer.data})

    def put(self, request, *args, **kwargs):
        q_id = kwargs.get('id', None)
        request.data['author'] = request.user.id

        if not q_id:
            return Response({'error': "Method \"Put\" is not allowed."})

        try:
            instance = Question.objects.get(id=q_id)
        except Exception:
            return Response({"error": "This Question does not exists."})

        serializer = QuestionSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"question": serializer.data})


class CategoryListAPIView(CategoryMixin, generics.ListAPIView):
    pass
