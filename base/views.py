from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Meeting, Question, Vote, Material, Division, Topic
from .serializers import MeetingSerializer, QuestionSerializer, VoteSerializer, TopicSerializer, MaterialSerializer
from django.core.files import File
import docx


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_vote(request, question_key):
    try: question = Question.objects.get(id=question_key)
    except: return HttpResponseNotFound()

    if question not in get_user_questions(request):
        return Response({'message': 'Not allowed to vote'}, status=status.HTTP_400_BAD_REQUEST)

    if Vote.objects.filter(user=request.user, question=question).exists():
        return Response({'message': 'Already voted'}, status=status.HTTP_400_BAD_REQUEST)

    vote = Vote(
        decision=request.POST['decision'],
        proposal=request.POST['proposal'],
        user=request.user,
        question=question,
    )
    vote.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_meeting(request):
    serializer = MeetingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_material(request):
    serializer = MaterialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def set_ready(request, key):
    try: meeting = Meeting.objects.get(id=key)
    except: return HttpResponseNotFound()

    meeting.is_quorum = True
    meeting.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def set_finished(request, key):
    try: meeting = Meeting.objects.get(id=key)
    except: return HttpResponseNotFound()

    meeting.is_finished = True
    meeting.time_end = datetime.now().time().replace(microsecond=0)

    if not meeting.is_quorum:
        content = 'Заседание не состоялось, не был достигнут кворум'
    else:
        content = 'Дата проведения общего собрания: ' + str(meeting.date) + \
                  '\nВремя начала: ' + str(meeting.time_start) + \
                  '\nВремя окончания: ' + str(meeting.time_end) + '\n\n'

        questions = Question.objects.filter(meeting=meeting)
        for question in questions:
            content += str(question.name) + ' (' + str(question.topic) + ')\n'
            votes = Vote.objects.filter(question=question)
            for vote in votes:
                content += '   ' + str(vote.user.first_name) + ' ' + str(vote.user.last_name) + ' - '
                if vote.agree and not vote.disagree:
                    content += 'За\n'
                elif vote.disagree and not vote.agree:
                    content += 'Против\n'
                else:
                    content += 'Воздержался\n'
            content += 'За - ' + str(votes.filter(agree=True).count()) + '  '
            content += 'Против - ' + str(votes.filter(disagree=True).count()) + '  '
            content += 'Воздержались - ' + str(votes.filter(agree=False, disagree=False).count()) + '  '
            content += '\n\n'

    name = ''
    if meeting.division.name == 'Акционеры':
        name += '01-'
    elif meeting.division.name == 'Директора':
        name += '02-'

    if meeting.is_scheduled is None:
        name += '00-'
    elif meeting.is_scheduled:
        name += '01-'
    else:
        name += '02-'

    if meeting.is_quorum:
        name += '01-'
    else:
        name += '00-'
    name += str(meeting.project_number)
    name += '-'
    name += str(meeting.date)

    mydoc = docx.Document()
    mydoc.add_paragraph(content)
    mydoc.save('documents/'+name+'.docx')

    meeting.protocol = 'documents/'+name+'.docx'

    meeting.save()
    return HttpResponse(content)
