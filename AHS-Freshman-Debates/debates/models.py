#!/usr/bin/env python3.4
#file: models.py

from django.contrib.auth.models import User
from django.db.models import ( Model, ForeignKey, IntegerField,
                               ManyToManyField, BooleanField, CharField,
                               TextField, DateTimeField, OneToOneField )

#User contains: username, password, email, first_name, last_name, groups,
#user_permissions, is_staff, is_active, last_login, date_joined

class Teacher(Model):
    user = OneToOneField(User)

class Judge(Model):
    user = OneToOneField(User)

class Debater(Model):
    user = OneToOneField(User)
    english_teacher = ForeignKey(Teacher, related_name='english_students')
    english_period = IntegerField()
    ihs_teacher = ForeignKey(Teacher, related_name='ihs_students')
    ihs_period = IntegerField()
    #TODO, attendance
    #attendance = ?

class Topic(Model):
    name        = CharField(max_length=25)
    description = CharField(max_length=150)

    def __str__(self):
        return '%s' % self.topic
   
class Team(Model):
    members = ManyToManyField(Debater)
    topic = ForeignKey(Topic)
    is_aff = BooleanField()
    teachers = ManyToManyField(Teacher)

    def __str__(self):
        return '%s' % self.team_number

#TODO, can subscores and deductions be done more elegantly, not making them
#models?
class Deduction(Model):
    value = IntegerField()
    notes = TextField()

class Subscore(Model):
    raw = IntegerField()
    deductions = ManyToManyField(Deduction)

    #get the final score after deductions have been accounted for
    def get_final(self):
        final = self.raw
        for d in self.deductions.all():
            final -= d.value
        return final

class Score(Model):
    subscores = ManyToManyField(Subscore)
    team = CharField(max_length=2)
    notes = TextField()

    def __str__(self):
        return '%s' % self.team_number

class Location(Model):
    location = CharField(max_length=255)

    def __str__(self):
        return '%s' % self.location

class Period(Model):
    period = IntegerField(max_length=2)

    def __str__(self):
        return '%s' % self.period
    
class Debate(Model):
    affirmative_team = ForeignKey(Team, related_name='aff_debate')
    negative_team = ForeignKey(Team, related_name='neg_debate')
    date = DateTimeField()
    location = ForeignKey(Location)
    period = IntegerField()
    topic = ForeignKey(Topic)
    judge = ManyToManyField(Judge)
    spectators = ManyToManyField(Team, blank=True)

    def __str__(self):
        return '%s' % self.topic
