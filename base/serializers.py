from rest_framework.serializers import ModelSerializer
from .models import Meeting, Question, Vote, Topic


class MeetingSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']
