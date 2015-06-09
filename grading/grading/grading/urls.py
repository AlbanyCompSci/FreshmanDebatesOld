from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'grading.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', 'usermanage.views.login'),
    url(r'^lessons/', 'lessons.views.lessons_overview'),
    url(r'^lesson/(?P<id>[0-9]+)/$', 'lessons.views.lesson'),
    url(r'^lesson/new/(?P<id>[0-9]+)/$', 'lessons.views.new_lesson'),
    url(r'^lesson/edit-(?P<id>[0-9]+)/$', 'lessons.views.edit_lesson'),
    url(r'^question/(?P<class_id>[0-9]+)-(?P<id>[0-9]+)/$', 'lessons.views.grade_question'),

    url(r'^class/new/$', 'usermanage.views.new_class'),
    url(r'^join/(?P<id>[0-9]+)/$', 'usermanage.views.join_class'),

    url(r'^mark-seen/$', 'lessons.views.mark_response_seen'),
    url(r'^save-comment/$', 'lessons.views.save_comment'),
    url(r'^save-responses/$', 'lessons.views.save_responses'),
)
