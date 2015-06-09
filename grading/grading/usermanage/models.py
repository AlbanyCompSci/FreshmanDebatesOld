from django.db import models
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User


class SchoolClass(models.Model):
    name = models.CharField(max_length=255)
    teachers = models.ManyToManyField(User, related_name='teachers')
    students = models.ManyToManyField(User, related_name='students')
    password = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'<SchoolClass: %r>' % (self.name)

    def get_join_url(self):
        return 'http://%s/join/%s/' % (get_current_site(None), self.id)

    def get_new_lesson_url(self):
        return '/lesson/new/%i/' % (self.id)
