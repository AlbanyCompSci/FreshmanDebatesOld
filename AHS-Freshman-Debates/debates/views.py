#!/usr/bin/env python3.4
#file: views.py

from django.contrib.auth.decorators import (permission_required, 
                                            user_passes_test,
                                            login_required)
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.conf import settings
from debates.forms import ScoreForm
from logging import getLogger

from social.backends.google import GooglePlusAuth

logger = getLogger('logview.debugger')

def login(request):
    if request.user.is_authenticated():
        logger.debug('User: ' + str(request.user))
        if request.user.groups.filter(name='admins').count():
            return redirect('/admin')
        if request.user.groups.filter(name='teachers').count():
            return redirect('/teacher')
        if request.user.groups.filter(name='judges').count():
            return redirect('/judge')
        if request.user.groups.filter(name='debaters').count():
            return redirect('/debater')
        else:
            return redirect('/spectator')
    else:
        return render_to_response('debates/login.html', {
            'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
            'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
            }, RequestContext(request))

def logout(request):
    auth_logout(request)
    return render_to_response('debates/login.html', {
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        }, RequestContext(request))

#menu for a teacher, shows teams
@user_passes_test(lambda u: u.groups.all().filter(name='teachers').count(), login_url='/')
def teacher(request):
    return render_to_response('debates/teacher.html', {
        'user': request.user,
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
    }, RequestContext(request))

#(teacher) view details on a team
@permission_required('debates.view_team', login_url='/')
def view_team(request):
    return

#menu for a judge, shows all debates that they have to score
@user_passes_test(lambda u: u.groups.all().filter(name='judges').count(), login_url='/')
def judge(request):
    #TODO, is all this necessary
    return render_to_response('debates/judge.html', {
        'user': request.user,
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
    }, RequestContext(request))


#(judge) submit scores for a debate
#@permission_required('debates.score_debate', login_url='/')
@user_passes_test(lambda u: u.groups.all().filter(name='judges').count(), login_url='/')
def score_debate(request):
    aff_form = ScoreForm()
    neg_form = ScoreForm()
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            s = form.save()
            #if the form is affirmative, set the object to be affirmative
            if 'form_affirmative' in request.POST:
                s.is_aff = True
                aff_form = form
            #else, assume its negative
            else:
                s.is_aff = False
                neg_form = form
            #save the form to the database
            s.save()
    forms = {
                'affirmative_form': aff_form,
                'negative_form':    neg_form
            }
    return render(request, 'debates/score_debate.html', forms)

#menu for a debater shows any relevant imformation (scores, debate details etc.)
@user_passes_test(lambda u: u.groups.all().filter(name='debaters').count(), login_url='/')
def debater(request):
    #TODO, is all this necessary
    return render_to_response('debates/debater.html', {
        'user': request.user,
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
    }, RequestContext(request))


#(debater, teacher) view score for a debate
@permission_required('debates.view_score', login_url='/')
def view_score(request):
    return

@user_passes_test(lambda u: u.is_authenticated(), login_url='/')
def spectator(request):
    return render_to_response('debates/spectator.html', {
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
        }, RequestContext(request))
