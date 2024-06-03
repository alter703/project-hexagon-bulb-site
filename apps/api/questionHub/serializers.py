from rest_framework import serializers

from apps.questionHub.models import Question, Category


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'author', 'category', 'title', 'content', 'is_closed')


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
