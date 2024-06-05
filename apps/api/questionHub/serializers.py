from rest_framework import serializers

from apps.questionHub.models import Question, Category


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'author', 'category', 'title', 'content', 'is_closed')

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.is_closed = validated_data.get("is_closed", instance.is_closed)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        return instance


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
