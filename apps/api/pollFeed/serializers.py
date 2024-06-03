from rest_framework import serializers

from apps.pollFeed.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'author', 'text', 'choices', 'created_at', 'is_closed')


# class CategorySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)