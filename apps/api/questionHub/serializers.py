from rest_framework import serializers

from apps.questionHub.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'category', 'title', 'content', 'is_closed')