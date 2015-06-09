from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from rest_framework import routers

from api_app import views

router = routers.DefaultRouter()
router.register(r'users',       views.UserViewSet      )
router.register(r'groups',      views.GroupViewSet     )
router.register(r'teams',       views.TeamViewSet      )
router.register(r'debates',     views.DebateViewSet    )
router.register(r'scores',      views.ScoreViewSet     )
router.register(r'evaluations', views.EvaluationViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DebatesDjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
)
