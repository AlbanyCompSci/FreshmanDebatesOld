#!/usr/bin/env python3.4
#file: forms.py

from django.forms           import ModelForm, ChoiceField, RadioSelect, Form
from django.db.models       import FileField
from debates.models         import Score, Team
from debates.merge_debaters import mergeDebaters

'''
SCORE_CHOICES = (
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10')
        )
ROLE_CHOICES = (
        ('0', 'School'),
        ('1', 'Teacher'),
        ('2', 'Judge'),
        ('3', 'Debater'),
        ('4', 'Admin'),
    )
scores = ChoiceField(widget=RadioSelect(), choices=SCORE_CHOICES)
'''

class ScoreForm(ModelForm):
    class Meta(object):
        model = Score

class TeamForm(ModelForm):
    class Meta(object):
        model = Team
