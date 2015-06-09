from django.contrib.auth.models import User
from django.db.models import ( CharField
                             , DateTimeField
                             , ManyToManyField
                             , Model
                             , OneToOneField
                             , SmallIntegerField
                             , TextField
                             , ForeignKey
                             )

from rest_framework import permissions

SAFE   = ['GET', 'OPTIONS', 'HEAD', 'TRACE']
#UNSAFE = ['POST', 'PUT', 'DELETE', 'PATCH']

class DebateObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.policy(request.user, request.method)

class Team(Model):
    teachers = ManyToManyField(User, related_name='teachers')
    debaters = ManyToManyField(User, related_name='debaters')
    def policy(self, user, method):
        if method in SAFE:
            return user in self
        return user in teachers
    def __contains__(self, user):
        return (user in teachers or user in debaters)

class Evaluation(Model):
    points   = SmallIntegerField()
    comments = TextField()
    # TODO: sensible policy
    def policy(self, user, method):
        parent_score = None
        for s in Score.objects.all():
            if self in s:
                parent_score = s
                break
        # free evaluation (should not arise)
        if not parent_score:
            return True
        return parent_score.policy(user, method)

class Score(Model):
    judge     = ForeignKey(User) # to be set automatically on upload
    speakerA  = OneToOneField(Evaluation, related_name='speaker_A')
    speakerB  = OneToOneField(Evaluation, related_name='speaker_B')
    crossExam = OneToOneField(Evaluation, related_name='cross_exam')
    slideShow = OneToOneField(Evaluation, related_name='slide_show')
    rebuttal  = OneToOneField(Evaluation, related_name='rebuttal')
    argument  = OneToOneField(Evaluation, related_name='argument')
    # TODO: sensible policy
    def policy(self, user, method):
        parent_debate = None
        for d in Debate.objects.all():
            if self in d.affScores or self in d.negScores:
                parent_debate = d
                break
        # free score (should not arise)
        if not parent_debate:
            return True
        if method in SAFE:
            return user in parent_debate
        return user == parent_score.judge
    def __contains__(self, evaluation):
        eval_fields = [ self.speakerA
                      , self.speakerB
                      , self.crossExam
                      , self.slideShow
                      , self.rebuttal
                      , self.argument
                      ]
        return any(map(lambda e: e == evaluation, eval_fields))
    
class Debate(Model):
    title     = CharField(max_length=140)
    time      = DateTimeField()
    location  = CharField(max_length=140)
    judges    = ManyToManyField(User)
    affTeam   = OneToOneField(Team, related_name='aff_team')
    negTeam   = OneToOneField(Team, related_name='neg_team')
    affScores = ManyToManyField(Score, related_name='aff_scores')
    negScores = ManyToManyField(Score, related_name='neg_scores')
    def policy(self, user, method):
        if method in SAFE:
            return user in self
        return user in judges
    def __contains__(self, user):
        return (user in judges or user in affTeam or user in negTeam)
