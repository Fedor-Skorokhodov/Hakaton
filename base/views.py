from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Meeting, Question, Vote, Material, Division
from .serializers import MeetingSerializer, QuestionSerializer, VoteSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meeting(request, key):
    try:
        meeting = Meeting.objects.get(id=key)
    except:
        return HttpResponseNotFound()

    serializer = MeetingSerializer(meeting)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, key):
    try: question = Question.objects.get(id=key)
    except: return HttpResponseNotFound()

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_meetings(request):
    division = request.user.division
    meetings = Meeting.objects.filter(division=division)
    serializer = MeetingSerializer(meetings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_questions(request):
    division = request.user.division
    meetings = Meeting.objects.filter(division=division)
    questions = Question.objects.filter(meeting__in=meetings)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meeting_questions(request, key):
    meeting = Meeting.objects.get(id=key)
    questions = Question.objects.filter(meeting=meeting)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question_votes(request, key):
    question = Question.objects.fet(id=key)
    votes = Vote.objects.filter(question=question)
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_vote(request, question_key):
    try: question = Question.objects.get(id=question_key)
    except: return HttpResponseNotFound()

    if not question in get_user_questions(request):
        return HttpResponse('Not allowed to vote')

    if Vote.objects.filter(user=request.user, question=question).exists():
        return HttpResponse('Already voted')

    vote = Vote(decision=request.POST['decision'],
                proposal=request.POST['proposal'],
                user=request.user,
                question=question,
                )
    vote.save()

    return HttpResponse('Success')
