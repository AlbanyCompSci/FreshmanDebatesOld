
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from models import Assignment, Course, CourseInstructor, StudentCourse, Submission, SubmissionComment, UserProfile
from sourcetrans.macro_module import macros
import JeevesLib

@JeevesLib.supports_jeeves
def add_to_context(context_dict, request, template_name, profile, concretize):
    sym2 = JeevesLib.Namespace({'context_dict':context_dict, 'request':request, 'template_name':template_name, 'profile':profile, 'concretize':concretize}, 'add_to_context')
    sym2.sym = True
    sym2.sym1 = None
    sym2.template_name = JeevesLib.jfun(sym2.concretize, sym2.template_name)
    sym2.context_dict['concretize'] = sym2.concretize
    sym2.context_dict['is_admin'] = JeevesLib.jand(JeevesLib.supports_jeeves((lambda: (sym2.profile != None))), JeevesLib.supports_jeeves((lambda: (sym2.profile.level == 'chair'))))
    sym2.context_dict['profile'] = sym2.profile
    sym2.context_dict['is_logged_in'] = JeevesLib.jand(JeevesLib.supports_jeeves((lambda: sym2.request.user)), JeevesLib.supports_jeeves((lambda: JeevesLib.jfun(JeevesLib.jand, JeevesLib.supports_jeeves((lambda: JeevesLib.jfun(sym2.request.user.is_authenticated))), JeevesLib.supports_jeeves((lambda: JeevesLib.jnot(JeevesLib.jfun(sym2.request.user.is_anonymous))))))))
    return sym2.sym1
'\nWraps around a request by getting the user and defining functions like\nconcretize.\n'

def request_wrapper(view_fn, *args, **kwargs):

    def real_view_fn(request):
        try:
            profile = UserProfile.objects.get(username=request.user.username)
            ans = view_fn(request, profile, *args, **kwargs)
            template_name = ans[0]
            context_dict = ans[1]
            if (template_name == 'redirect'):
                path = context_dict
                return HttpResponseRedirect(JeevesLib.concretize(profile, path))
            concretizeState = JeevesLib.jeevesState.policyenv.getNewSolverState(profile)

            def concretize(val):
                return concretizeState.concretizeExp(val, JeevesLib.jeevesState.pathenv.getEnv())
            add_to_context(context_dict, request, template_name, profile, concretize)
            return render_to_response(template_name, RequestContext(request, context_dict))
        except Exception:
            import traceback
            traceback.print_exc()
            raise
        finally:
            JeevesLib.clear_cache()
    real_view_fn.__name__ = view_fn.__name__
    return real_view_fn

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def index(request, user_profile):
    sym5 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'index')
    sym5.sym3 = True
    sym5.sym4 = None
    sym5.sym4 = ('index.html', {'name':sym5.user_profile.name})
    sym5.sym3 = False
    return sym5.sym4
'\nLooking at an assignment. Different users have different policies.\n'

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def assignments_view(request, user_profile):
    sym8 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'assignments_view')
    sym8.sym6 = True
    sym8.sym7 = None
    sym8.course_id = JeevesLib.jfun(sym8.request.GET.get, 'course_id')
    sym8.course = JeevesLib.jfun(Course.objects.get, jeeves_id=sym8.course_id)
    sym8.assignments = JeevesLib.jfun(JeevesLib.jfun(Assignment.objects.filter, course=sym8.course).all)
    sym8.idx = 0

    def sym9(a):
        sym8.a = a

        def sym10():
            sym8.a.label = ('collapse' + JeevesLib.jfun(str, sym8.idx))
            sym8.idx += 1

        def sym11():
            pass
        JeevesLib.jif(sym8.sym6, sym10, sym11)
    JeevesLib.jmap(sym8.assignments, sym9)

    def sym12():
        sym8.scs = JeevesLib.jfun(JeevesLib.jfun(StudentCourse.objects.filter, course=sym8.course).all)
        sym8.sym7 = ('course_assignments.html', {'assignments':sym8.assignments, 'scs':sym8.scs})
        sym8.sym6 = False

    def sym13():
        pass
    JeevesLib.jif(sym8.sym6, sym12, sym13)
    return sym8.sym7

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def courses_view(request, user_profile):
    sym16 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'courses_view')
    sym16.sym14 = True
    sym16.sym15 = None
    sym16.studentcourses = JeevesLib.jfun(JeevesLib.jfun(StudentCourse.objects.filter, student=sym16.user_profile).all)
    sym16.courses = JeevesLib.JList([])

    def sym17(sc):
        sym16.sc = sc

        def sym18():
            sym16.c = sym16.sc.course
            sym16.c.grade = sym16.sc.grade
            sym16.c.instructors = JeevesLib.JList([])
            sym16.courseInstructors = JeevesLib.jfun(list, JeevesLib.jfun(CourseInstructor.objects.filter, course=sym16.c))

            def sym20(ci):
                sym16.ci = ci

                def sym21():
                    JeevesLib.jfun(sym16.c.instructors.append, sym16.ci.instructor)

                def sym22():
                    pass
                JeevesLib.jif(sym16.sym14, sym21, sym22)
            JeevesLib.jmap(sym16.courseInstructors, sym20)

            def sym23():
                JeevesLib.jfun(sym16.courses.append, sym16.c)

            def sym24():
                pass
            JeevesLib.jif(sym16.sym14, sym23, sym24)

        def sym19():
            pass
        JeevesLib.jif(sym16.sym14, sym18, sym19)
    JeevesLib.jmap(sym16.studentcourses, sym17)

    def sym25():
        sym16.sym15 = ('courses.html', {'name':sym16.user_profile.name, 'courses':sym16.courses, 'which_page':'courses'})
        sym16.sym14 = False

    def sym26():
        pass
    JeevesLib.jif(sym16.sym14, sym25, sym26)
    return sym16.sym15

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def submission_view(request, user_profile):
    sym29 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'submission_view')
    sym29.sym27 = True
    sym29.sym28 = None
    sym29.submission_id = JeevesLib.jfun(sym29.request.GET.get, 'submission_id')
    sym29.submission = JeevesLib.jfun(Submission.objects.get, jeeves_id=sym29.submission_id)
    sym29.comments = JeevesLib.jfun(SubmissionComment.objects.filter, submission=sym29.submission)
    sym29.sym28 = ('submission.html', {'submission':sym29.submission, 'comments':sym29.comments, 'comments_length':JeevesLib.jfun(len, sym29.comments)})
    sym29.sym27 = False
    return sym29.sym28

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def submissions_view(request, user_profile):
    sym32 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'submissions_view')
    sym32.sym30 = True
    sym32.sym31 = None
    sym32.user_submissions = JeevesLib.jfun(JeevesLib.jfun(Submission.objects.filter, author=sym32.user_profile).all)
    sym32.sym31 = ('submissions.html', {'submissions':sym32.user_submissions, 'which_page':'submissions'})
    sym32.sym30 = False
    return sym32.sym31

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def profile_view(request, user_profile):
    sym35 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'profile_view')
    sym35.sym33 = True
    sym35.sym34 = None

    def sym36():
        sym35.username = JeevesLib.jfun(sym35.request.GET.get, 'username', '')

        def sym38():
            sym35.profile = JeevesLib.jfun(UserProfile.objects.get, username=sym35.username)

        def sym39():
            sym35.profile = sym35.user_profile
        JeevesLib.jif((sym35.username != ''), sym38, sym39)

        def sym40():
            pass

        def sym41():
            pass
        JeevesLib.jif(sym35.sym33, sym40, sym41)

    def sym37():
        sym35.profile = sym35.user_profile
    JeevesLib.jif((sym35.request.method == 'GET'), sym36, sym37)

    def sym42():

        def sym44():
            assert (sym35.username == sym35.user_profile.username)
            sym35.user_profile.email = JeevesLib.jfun(sym35.request.POST.get, 'email', '')
            sym35.user_profile.name = JeevesLib.jfun(sym35.request.POST.get, 'name', '')
            sym35.user_profile.role = JeevesLib.jfun(sym35.request.POST.get, 'role', '')
            JeevesLib.jfun(sym35.user_profile.save)

        def sym45():
            pass
        JeevesLib.jif((sym35.request.method == 'POST'), sym44, sym45)

        def sym46():
            sym35.sym34 = ('profile.html', {'user_profile':sym35.profile, 'name':sym35.profile.name, 'which_page':'profile'})
            sym35.sym33 = False

        def sym47():
            pass
        JeevesLib.jif(sym35.sym33, sym46, sym47)

    def sym43():
        pass
    JeevesLib.jif(sym35.sym33, sym42, sym43)
    return sym35.sym34

def register_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('index')
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            User.objects.create(username=user.username, email=request.POST.get('email', ''), name=request.POST.get('name', ''), role=request.POST.get('role', ''))
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('index')
    else:
        form = UserCreationForm()
    return render_to_response('registration/account.html', RequestContext(request, {'form':form, 'which_page':'register'}))