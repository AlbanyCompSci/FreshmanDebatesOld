from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    school_class = models.ForeignKey('usermanage.SchoolClass')
    questions = models.ManyToManyField('lessons.Question')

    def __unicode__(self):
        return u'<Lesson: %r>' % (self.name)

    def get_absolute_url(self):
        return '/lesson/%i/' % (self.id)

    def get_edit_url(self):
        return '/lesson/edit-%i/' % (self.id)


class Question(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u'<Question: %r>' % (self.title)


class Response(models.Model):
    # TODO: some of these columns are null for bad reasons
    # (i.e. I don't want to throw away existing migration
    # scripts)
    text = models.TextField(blank=True, null=True)
    answerer = models.ForeignKey(User, null=True)
    question = models.ForeignKey('lessons.Question', null=True)
    comment = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)

    # needed to connect a response to a class
    lesson = models.ForeignKey('lessons.Lesson', null=True)

    def __unicode__(self):
        return u'<Response: %r>' % (self.question.title)
