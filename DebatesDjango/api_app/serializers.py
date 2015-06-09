from django.contrib.auth.models import User, Group

from rest_framework import serializers

from api_app.models import Team, Debate, Score, Evaluation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Group
        fields = ('url', 'name')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Team
        fields = ('url', 'teachers', 'debaters')

class EvaluationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Evaluation
        fields = ('url', 'points', 'comments')

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Score
        fields = ( 'url'
                 , 'speakerA'
                 , 'speakerB'
                 , 'crossExam'
                 , 'slideShow'
                 , 'rebuttal'
                 , 'argument'
                 , 'judge'
                 )

class DebateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Debate
        fields = ( 'url'
                 , 'time'
                 , 'judges'
                 , 'affTeam'
                 , 'negTeam'
                 , 'affScores'
                 , 'negScores'
                 )
