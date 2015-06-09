from django.contrib.auth.models import User, Group
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import mixins

from api_app.models import Team, Debate, Score, Evaluation

from api_app.serializers import ( UserSerializer
                                , GroupSerializer
                                , TeamSerializer
                                , DebateSerializer
                                , ScoreSerializer
                                , EvaluationSerializer
                                )

# API endpoints

class UserViewSet(viewsets.ModelViewSet):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset         = Group.objects.all()
    serializer_class = GroupSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset         = Team.objects.all()
    serializer_class = TeamSerializer

class DebateViewSet(viewsets.ModelViewSet):
    queryset         = Debate.objects.all()
    serializer_class = DebateSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset         = Score.objects.all()
    serializer_class = ScoreSerializer

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset         = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
