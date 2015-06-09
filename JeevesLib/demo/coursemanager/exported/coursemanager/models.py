
from django.conf import settings
from django.db.models import CharField, DateTimeField, FileField, IntegerField, TextField
from jeevesdb.JeevesModel import JeevesModel as Model, JeevesForeignKey as ForeignKey
from jeevesdb.JeevesModel import label_for
import os
from sourcetrans.macro_module import macros
import JeevesLib
ROLE = (('s', 'Student'), ('i', 'Instructor'), ('a', 'Admin'))
GRADE = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('U', 'Unknown'))

class UserProfile(Model):
    username = CharField(max_length=1024)
    email = CharField(max_length=1024)
    name = CharField(max_length=1024)
    role = CharField(max_length=1, choices=ROLE)

    @staticmethod
    def jeeves_get_private_email(user):
        return '[redacted]'

    @staticmethod
    @label_for('email')
    @JeevesLib.supports_jeeves
    def jeeves_restrict_userprofilelabel(user, ctxt):
        sym2 = JeevesLib.Namespace({'user':user, 'ctxt':ctxt}, 'jeeves_restrict_userprofilelabel')
        sym2.sym = True
        sym2.sym1 = None
        sym2.sym1 = (sym2.user == sym2.ctxt)
        sym2.sym = False
        return sym2.sym1

    @JeevesLib.supports_jeeves
    def is_instructor(self, course):
        sym5 = JeevesLib.Namespace({'self':self, 'course':course}, 'is_instructor')
        sym5.sym3 = True
        sym5.sym4 = None
        sym5.sym4 = (JeevesLib.jfun(CourseInstructor.objects.get, course=sym5.course, instructor=sym5.self) != None)
        sym5.sym3 = False
        return sym5.sym4

    class Meta:
        db_table = 'coursemanager_userprofile'

class Course(Model):
    name = CharField(max_length=1024)
    courseId = CharField(max_length=1024)

class CourseInstructor(Model):
    course = ForeignKey(Course, null=True, related_name='courseinstructor_course')
    instructor = ForeignKey(UserProfile, null=True, related_name='courseinstructor_instructor')

class StudentCourse(Model):
    student = ForeignKey(UserProfile, null=True, related_name='students')
    course = ForeignKey(Course, null=True, related_name='studentcourse_course')
    grade = CharField(max_length=1, choices=GRADE)

    @staticmethod
    def jeeves_get_private_grade(sc):
        return 'U'

    @staticmethod
    @label_for('grade')
    @JeevesLib.supports_jeeves
    def jeeves_restrict_grade(sc, ctxt):
        sym8 = JeevesLib.Namespace({'sc':sc, 'ctxt':ctxt}, 'jeeves_restrict_grade')
        sym8.sym6 = True
        sym8.sym7 = None
        'Only the student can see the grade.\n\t'
        sym8.sym7 = JeevesLib.jor(JeevesLib.supports_jeeves((lambda: (sym8.sc.student == sym8.ctxt))), JeevesLib.supports_jeeves((lambda: JeevesLib.jfun(sym8.ctxt.is_instructor, sym8.sc.course))))
        sym8.sym6 = False
        return sym8.sym7

    class Meta:
        db_table = 'coursemanager_studentcourse'

class Assignment(Model):
    name = CharField(max_length=1024)
    dueDate = DateTimeField()
    maxPoints = IntegerField()
    prompt = TextField()
    owner = ForeignKey(UserProfile, null=True, related_name='assignment_user')
    course = ForeignKey(Course, null=True, related_name='assignment_course')

    @JeevesLib.supports_jeeves
    def get_average(self):
        sym11 = JeevesLib.Namespace({'self':self}, 'get_average')
        sym11.sym9 = True
        sym11.sym10 = None
        sym11.submissions = JeevesLib.jfun(JeevesLib.jfun(Submission.objects.filter, assignment=sym11.self).all)
        sym11.scores = JeevesLib.jfun(JeevesLib.jmap, sym11.submissions, JeevesLib.supports_jeeves((lambda s: s.score)))
        sym11.sum_scores = 0.0

        def sym12(s):
            sym11.s = s

            def sym13():
                sym11.sum_scores += sym11.s.score
                sym11.sym10 = JeevesLib.jif((sym11.scores.__len__ == 0), JeevesLib.supports_jeeves((lambda: 0.0)), JeevesLib.supports_jeeves((lambda: (sym11.sum_scores / sym11.scores.__len__))))
                sym11.sym9 = False

            def sym14():
                pass
            JeevesLib.jif(sym11.sym9, sym13, sym14)
        JeevesLib.jmap(sym11.submissions, sym12)

        def sym15():
            pass

        def sym16():
            pass
        JeevesLib.jif(sym11.sym9, sym15, sym16)
        return sym11.sym10
    '\n    @jeeves\n    def std(self):\n\tsubmissions = Submissions.objects.filter(assignment=self).all()\n\tmean = self.average(l)\n\tvariance = map(lambda x: (float(x) - mean)**2, l)\n\tstdev = math.sqrt(self.average(variance))\n\treturn stdev #check precision\n    '
    '\n    @jeeves\n    def median(self, l):\n\tsortedL = sorted(l)\n\tlength = len(sortedL)\n\tif length % 2:\n            return sortedL[length / 2]\n\telse:\n\t    return self.average( sortedL[length / 2], sortedL[length/2 - 1] )\n    '

class Submission(Model):
    assignment = ForeignKey(Assignment, null=True, related_name='submission_assignment')
    author = ForeignKey(UserProfile, null=True, related_name='submission_author')
    uploadFile = FileField(upload_to='submissions')
    submitDate = DateTimeField(auto_now=True)
    grade = CharField(max_length=1, choices=GRADE)
    score = IntegerField()

    @staticmethod
    def jeeves_get_private_uploadFile(s):
        return None

    @staticmethod
    def jeeves_get_private_grade(s):
        return 'U'

    @staticmethod
    @label_for('uploadFile', 'grade')
    @JeevesLib.supports_jeeves
    def jeeves_restrict_uploadFile(s, ctxt):
        sym19 = JeevesLib.Namespace({'s':s, 'ctxt':ctxt}, 'jeeves_restrict_uploadFile')
        sym19.sym17 = True
        sym19.sym18 = None
        sym19.sym18 = JeevesLib.jor(JeevesLib.supports_jeeves((lambda: (sym19.s.author == sym19.ctxt))), JeevesLib.supports_jeeves((lambda: JeevesLib.jfun(sym19.ctxt.is_instructor, sym19.s.assignment.course))))
        sym19.sym17 = False
        return sym19.sym18
COMMENT_PERMISSION = (('U', 'Only visible to user'), ('I', 'Only visible to instructors'), ('E', 'Visible to everyone'))

class SubmissionComment(Model):
    submission = ForeignKey(Submission, null=True, related_name='submissioncomment_submission')
    author = ForeignKey(UserProfile, null=True)
    submitDate = DateTimeField(auto_now=True)
    body = TextField()
    commentPermissions = CharField(max_length=1, choices=COMMENT_PERMISSION)
from django.dispatch import receiver
from django.db.models.signals import post_syncdb
import sys
current_module = sys.modules[__name__]

@receiver(post_syncdb, sender=current_module)
def dbSynced(sender, **kwargs):
    if settings.DEBUG:
        execfile(os.path.join(settings.BASE_DIR, '..', 'SampleData.py'))