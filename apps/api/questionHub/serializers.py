from rest_framework import serializers

from apps.questionHub.models import Question, Category

# class TestCategory:
#     def __init__(self, name) -> None:
#         self.name = name


class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = ('id', 'author', 'category', 'title', 'content', 'is_closed')


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


# def encode():
#     model = TestCategory('amogus')
#     serialized_model = CategorySerializer(model)
#     print(serialized_model.data, type(serialized_model),type(serialized_model.data), sep='\n\n')
