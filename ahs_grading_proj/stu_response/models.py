from django.db import models
from django.contrib.auth.models import User
from django import forms
import random
from hashlib import sha1
import datetime
from django.utils import timezone
from django.utils.timezone import utc


class Question(models.Model):
    text = models.CharField(max_length=2000)
    q_num = models.IntegerField()

    def __unicode__(self):
        return self.text

    def short_text(self):
        if len(self.text) < 15:
            return self.text
        else:
            return self.text[:12] + "..."


class Response(models.Model):
    question = models.ForeignKey(Question)
    student = models.ForeignKey(User)
    text = models.CharField(max_length=3000)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True)
    viewed = models.BooleanField(default=False)
    comment = models.CharField(default="", blank=True, max_length=3000)
    uid = models.CharField(null=True, blank=True, unique=True, max_length=200)

    def __unicode__(self):
        return "(" + self.student.username + ") " + self.text

    def save(self, set_date=None, *args, **kwargs):
        if self.uid is None or self.uid == "":
            uid = sha1(str(random.random())).hexdigest()
            while Response.objects.filter(uid=uid).count() > 0:
                uid = sha1(str(random.random())).hexdigest()
            self.uid = uid
        if set_date:
            self.edit_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(Response, self).save(*args, **kwargs)

    def getLesson(self):
        return self.question.lesson_set.all()[0]

    def is_blank(self):
        return self.text.strip() == ""

    def get_format_date(self):
        return timezone.make_naive(self.edit_date, timezone.get_current_timezone()).strftime("%b. %d, %Y, %I:%M %p")

    def cmp_and_viewed(self):
        return self.viewed and not self.is_blank()


class Lesson(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='created_lessons')
    questions = models.ManyToManyField(Question, blank=True)
    respondents = models.ManyToManyField(User, related_name='responded_lessons', blank=True)
    recorded_responses = models.ManyToManyField(Response, blank=True)
    key = models.CharField(unique=True, max_length=200)

    def __unicode__(self):
        return self.name

    def getStudentsResponded(self):
        respondents = sorted(self.respondents.all(), key=lambda r: r.last_name.lower())
        users = []
        for r in respondents:
            users.append(r)
        return users

    def getStudentsCompleted(self):
        students = sorted(self.respondents.all(), key=lambda r: r.last_name.lower())
        studentsDone = []
        for s in students:
            numDone = self.getNumCompleted(s.id)
            if numDone == self.questions.count():
                studentsDone.append(s)
        return studentsDone

    def getResponses(self, q_num=None, stu_id=None, order="-edit_date"):
        lesson_responses = []
        if q_num and self.questions.count() > 0:
            question = self.questions.get(q_num=q_num)
            responses = Response.objects.filter(question=question).exclude(text="").order_by(order)
            if order.find("student") != -1:
                reverse = False
                if order.find("-") != -1:
                    reverse = True
                responses = sorted(responses, key=lambda r: r.student.last_name.lower(), reverse=reverse)
            lesson_responses.append(responses)
        elif stu_id:
            student = User.objects.get(pk=stu_id)
            q_set = self.questions.all().order_by('q_num')
            for q in q_set:
                q_responses = Response.objects.filter(question=q, student=student).exclude(text="")
                if len(q_responses) != 0:
                    lesson_responses.append(q_responses)
        else:
            q_set = self.questions.all().order_by('q_num')
            for q in q_set:
                q_responses = Response.objects.filter(question=q).exclude(text="").order_by(order)
                if len(q_responses) != 0:
                    lesson_responses.append(q_responses)
        return lesson_responses

    def get_view_url(self):
        return "/lesson/" + self.key + "/"

    def get_edit_url(self):
        return "/lesson/edit/" + self.key + "/"

    def get_response_url(self):
        return "/responses/" + self.key + "/"

    def get_stu_url(self):
        return "/ajax/lesson/" + self.key + "/students/"

    def getNumCompleted(self, user_id):
        user = User.objects.get(pk=user_id)
        responses = self.recorded_responses.filter(student=user)
        completed = 0
        for r in responses:
            if not r.is_blank():
                completed += 1
        return completed

    # Temporary method to ease migration to new student getting system
    def addPrevResponses(self):
        users = []
        for r in self.recorded_responses.all():
            if r.student not in users:
                users.append(r.student)
        for u in users:
            self.respondents.add(u)

    def save(self, *args, **kwargs):
        if self.key is None or self.key == "":
            key = sha1(str(random.random())).hexdigest()
            while Lesson.objects.filter(key=key).count() > 0:
                key = sha1(str(random.random())).hexdigest()
            self.key = key
        super(Lesson, self).save(*args, **kwargs)


def responsesAllViewed(user, lesson):
    for response in lesson.recorded_responses.filter(student=user):
        if not response.is_blank() and not response.viewed:
            return False
    return True


def fixResponses():
    for l in Lesson.objects.all():
        l.addPrevResponses()


def getPercentComplete(user, lesson):
    total = lesson.questions.count()
    completed = lesson.getNumCompleted(user_id=user.id)
    return completed * 1.0 / total


def getRespondedLessons(user):
    all_lessons = []
    responded_lessons = user.responded_lessons.order_by('-creation_date')
    class_lessons = []
    for c in user.class_set.all():
        class_lessons.append(c.lessons.all())
    for lesson_set in class_lessons:
        for l in lesson_set:
            all_lessons.append(l)
    for l in responded_lessons:
        if l not in all_lessons:
            all_lessons.append(l)
    return all_lessons


class Class(models.Model):
    name = models.CharField(max_length=100, help_text='Name of the class')
    creator = models.ForeignKey(User, related_name='+', editable=False)
    description = models.CharField(max_length=2000, help_text='A short description.')
    teachers = models.ManyToManyField(User, related_name='+', blank=True)
    students = models.ManyToManyField(User, blank=True)
    password = models.CharField(max_length=50, help_text='A password required to the class.')
    lessons = models.ManyToManyField(Lesson, blank=True, help_text="Select lessons to be seen by this class.")
    uid = models.CharField(max_length=200, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Classes"

    def save(self, *args, **kwargs):
        if self.uid is None or self.uid == "":
            key = hex(random.getrandbits(32)).rstrip("L").lstrip("0x")
            while Class.objects.filter(uid=key).count() > 0:
                key = hex(random.getrandbits(32)).rstrip("L").lstrip("0x")
            self.uid = key
        super(Class, self).save(*args, **kwargs)

    def get_view_url(self):
        return "/class/" + self.uid + "/"

    def get_edit_url(self):
        return "/class/edit/" + self.uid + "/"


class ClassRegistrationForm(forms.Form):
    password = forms.CharField(max_length=50)


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', 'description', 'password', 'lessons')
        widgets = {
            'description': forms.Textarea(attrs={"style": "resize:vertical;"}),
        }

    def __init__(self, creator, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        choices = Lesson.objects.filter(creator=creator)
        self.fields['lessons'].queryset = choices
        self.fields['lessons'].widget.attrs.update({'data-placeholder': 'Select lessons'})
        self.fields['lessons'].help_text = 'Select lessons to be seen by this class.'


class ClassStudentMCField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() + " (" + obj.username + ")"


class ClassEditForm(forms.ModelForm):
    students = ClassStudentMCField(queryset=None)

    class Meta:
        model = Class
        fields = ('name', 'description', 'password', 'lessons', 'students')
        widgets = {
            'description': forms.Textarea(),
        }

    def __init__(self, creator, *args, **kwargs):
        super(ClassEditForm, self).__init__(*args, **kwargs)
        c_choices = Lesson.objects.filter(creator=creator)
        self.fields['lessons'].queryset = c_choices
        s_choices = User.objects.filter(is_staff=False)
        self.fields['students'].queryset = s_choices
        self.fields['students'].widget.attrs.update({'data-placeholder': 'Select students'})
        self.fields['lessons'].widget.attrs.update({'data-placeholder': 'Select lessons'})
        self.fields['lessons'].help_text = 'Select lessons to be seen by this class.'
        self.fields['students'].help_text = 'Select students to be in this class.'


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('text',)
