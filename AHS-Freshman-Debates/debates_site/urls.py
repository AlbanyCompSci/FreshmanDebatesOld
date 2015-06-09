#!/usr/bin/env python3.4

from django.conf.urls import patterns, include, url
from django.contrib   import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'debates.views.login'),
    url(r'^login$', 'debates.views.login'),
    url(r'^logout$', 'debates.views.logout'),
    #admin
    url(r'^admin', include(admin.site.urls)),
    #admin documentation
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^teacher$', 'debates.views.teacher'),
    url(r'^view_team$', 'debates.views.view_team'),
    url(r'^judge$', 'debates.views.judge'),
    url(r'^score_debate$', 'debates.views.score_debate'),
    url(r'^debater$', 'debates.views.debater'),
    url(r'^view_score$', 'debates.views.view_score'),
    url(r'^spectator$', 'debates.views.spectator'),
    #url(r'^login-error/$', 'debates.views.login_error'),
    #add social name space for social authorization
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)
