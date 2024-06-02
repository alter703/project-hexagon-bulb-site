from rest_framework import serializers

from apps.questionHub.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = ('id', 'author', 'category', 'title', 'content', 'is_closed')