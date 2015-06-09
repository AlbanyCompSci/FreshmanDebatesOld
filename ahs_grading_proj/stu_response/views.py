from django.shortcuts import render_to_response, redirect, get_object_or_404
from stu_response.models import Lesson, Question, Response, getRespondedLessons, getPercentComplete, ClassForm, ClassEditForm, Class, ClassRegistrationForm, responsesAllViewed
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from django.forms.util import ErrorList, ErrorDict
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template import RequestContext
from django.contrib import messages
from django.utils.safestring import mark_safe
import itertools


@user_passes_test(lambda u: u.is_staff)
def createLesson(request):
    if(request.method == "POST"):
        questions = simplejson.loads(request.POST['questions'])
        lesson = Lesson(name=request.POST['lesson_name'], creator=User.objects.get(pk=request.user.id))
        lesson.save()
        for q in questions:
            if q['id'] == "":
                x = Question(text=q['q_text'], q_num=q['q_num'])
                x.save()
                lesson.questions.add(x)
            else:
                x = Question.objects.get(pk=q['id'])
                x.text = q['q_text']
                x.q_num = q['q_num']
                x.save()
        messages.add_message(request, messages.INFO, "Lesson \"" + lesson.name + "\" created.")
        return redirect('/')
    else:
        try:
            num = int(request.GET['num']) + 1
        except KeyError:
            num = 1
        return render_to_response("stu_response/lesson_form.html", {"num": range(1, num)}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def editLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)

    lesson_is_in = lesson.class_set.all()
    user_is_legit = False
    for cls in lesson_is_in:
        if request.user in cls.teachers.all():
            user_is_legit = True
    if not user_is_legit:
        return HttpResponseForbidden("You do not have access to this page.")

    if(request.method == "POST"):
        questions = simplejson.loads(request.POST['questions'])
        lesson.name = request.POST['lesson_name']
        lesson.save()
        addedQ = []
        for q in questions:
            if q['id'] == "":
                x = Question(text=q['q_text'], q_num=q['q_num'])
                x.save()
                lesson.questions.add(x)
            else:
                if lesson.questions.filter(pk=q['id']).count() == 0:
                    return HttpResponseForbidden("Stop screwing with us")
                x = Question.objects.get(pk=q['id'])
                x.text = q['q_text']
                x.q_num = int(q['q_num'])
                x.save()
            addedQ.append(x)
        q_set = lesson.questions.all()
        for x in q_set:
            for q in range(len(addedQ)):
                if x.id.__str__() == addedQ[q].id.__str__():
                    break
                elif q == len(questions) - 1:
                    x.delete()
                    break
        messages.add_message(request, messages.INFO, lesson.name + " saved.")
        return redirect('/')
    return render_to_response("stu_response/lesson_form.html", {"questions": lesson.questions.all().order_by("q_num"), "lesson": lesson}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def deleteLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)

    if lesson.creator == request.user:
        lesson.recorded_responses.all().delete()
        lesson.questions.all().delete()
        lesson.delete()
        messages.success(request, "Lesson successfully deleted.")
        return HttpResponse(simplejson.dumps({"success": True}), mimetype="application/json")
    else:
        return HttpResponseForbidden(simplejson.dumps({"success": False}), mimetype="application/json")


@login_required
def viewLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    responses = []
    if lesson.recorded_responses.filter(student=User.objects.get(pk=request.user.id)):
        for q in lesson.questions.all().order_by("q_num"):
            try:
                r = Response.objects.get(question=q, student=User.objects.get(pk=request.user.id))
            except ObjectDoesNotExist:
                r = Response(student=User.objects.get(pk=request.user.id), text="", question=q)
                r.save(set_date=True)
            except MultipleObjectsReturned:
                temp = Response.objects.filter(question=q, student=User.objects.get(pk=request.user.id)).order_by("edit_date")
                for x in temp:
                    if x != temp[temp.count() - 1]:
                        x.delete()
                    else:
                        r = x
            curr = {
                "user_id": r.student.__unicode__(),
                "response": r.text,
                "last_edit": r.edit_date.__str__(),
                "q_num": r.question.q_num.__str__(),
                "comment": r.comment,
            }
            responses.append(curr)
    if request.method == "POST":
        if request.user not in lesson.respondents.all():
            lesson.respondents.add(request.user)
        responses = simplejson.loads(request.POST['responses'])
        for r in responses:
            changed = False

            temp = lesson.questions.filter(pk=r['id']).count()
            if request.is_ajax() and temp == 0:
                return HttpResponseForbidden(simplejson({"success": False}), mimetype="application/json")
            elif temp == 0:
                return HttpResponseForbidden("Stop screwing with us")

            if Response.objects.filter(student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id'])).count() > 0:
                response = Response.objects.get(student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id']))
                if response.text != r['response']:
                    response.viewed = False
                    response.text = r['response']
                    changed = True
            else:
                response = Response(text=r['response'], student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id']))
                changed = True
            if changed:
                response.save(set_date=True)
                lesson.recorded_responses.add(response)
        if request.is_ajax():
            return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')
        messages.success(request, "Responses successfully recorded.")
    return render_to_response("stu_response/lesson_view.html", {"lesson": lesson, "questions": lesson.questions.all().order_by('q_num'), "responses": simplejson.dumps(responses)}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def viewResponses(request, lesson_id, q_num=None, stu_id=None):
    lesson = get_object_or_404(Lesson, key=lesson_id)

    lesson_is_in = lesson.class_set.all()
    user_is_legit = False
    for cls in lesson_is_in:
        if request.user in cls.teachers.all():
            user_is_legit = True
    if not user_is_legit:
        return HttpResponseForbidden("You do not have access to this page.")
    lesson_set = lesson.questions.all().order_by('q_num')
    classes = lesson.class_set.all()
    curr_q = None
    if q_num and lesson.questions.count() > 0:
        curr_q = lesson.questions.get(q_num=q_num)
    elif lesson.questions.count() == 0:
        messages.error(request, mark_safe("You need to add questions to this lesson before you get responses! <a href='" + lesson.get_edit_url() + "'>Edit Lesson</a>"))
    return render_to_response("stu_response/response_view.html", {"questions": lesson_set, "classes": classes, "lesson_key": lesson_id, "question": curr_q, "lesson": lesson, "lesson_id": lesson.id, "users": lesson.getStudentsResponded()}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def createComment(request, response_id):
    # Error Codes:
    # 0 - Same comment already exists
    # 1 - All other errors
    response = get_object_or_404(Response, uid=response_id)
    if request.method == "POST" and request.POST.get("comment", False) or request.POST.get("comment") == "":
        if response.comment == request.POST.get("comment"):
            return HttpResponse(simplejson.dumps({"success": False, "errorCode": 0}), mimetype="application/json")
        response.comment = request.POST.get("comment")
        response.save()
        return HttpResponse(simplejson.dumps({"success": True}), mimetype="application/json")
    return HttpResponse(simplejson.dumps({"success": False, "errorCode": 0}), mimetype="application/json")


@user_passes_test(lambda u: u.is_staff)
def createClass(request):
    if request.method == "POST":
        form = ClassForm(data=request.POST, creator=request.user)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.creator = request.user
            new_class.save()
            for l in form.cleaned_data['lessons']:
                new_class.lessons.add(l)
            messages.success(request, "Class \"" + new_class.name + "\"created.")
            return redirect('/account/classes/')
    else:
        form = ClassForm(creator=request.user)
    return render_to_response("stu_response/class_form.html", {"form": form, "submit_text": "Add Class"}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def editClass(request, class_id):
    c = get_object_or_404(Class, uid=class_id)
    if(request.user == c.creator):
        if request.method == "POST":
            form = ClassEditForm(data=request.POST, instance=c, creator=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Class saved.")
                return redirect('/account/classes/')
        else:
            form = ClassEditForm(instance=c, creator=request.user)
        return render_to_response('stu_response/class_form.html', {"class": c, "form": form, "submit_text": "Submit Class", "title": "Edit question", "success": "false"}, context_instance=RequestContext(request))
    else:
        # Is the user is not the creator of the question (or staff)
        return redirect('/')


@user_passes_test(lambda u: u.is_staff)
def deleteClass(request, class_id):
    c = get_object_or_404(Class, uid=class_id)
    if c.creator == request.user:
        c.delete()
        if request.is_ajax():
            return HttpResponse(simplejson.dumps({"success": True}), mimetype="application/json")
        else:
            messages.success(request, "Class deleted.")
            return redirect('/account/classes/')
    if request.is_ajax():
        return HttpResponseForbidden(simplejson.dumps({"success": False}), mimetype="application/json")
    return redirect('/account/classes/')


@login_required
def removeSelfFromClass(request, class_id):
    c = get_object_or_404(Class, uid=class_id)
    if request.user in c.students.all():
        c.students.remove(request.user)
    return redirect('/account/classes/')


@login_required
def listClasses(request):
    if request.user.is_staff:
        classes = Class.objects.filter(creator=request.user)
    else:
        classes = request.user.class_set.all()
    return render_to_response('stu_response/class_list.html', {"classes": classes}, context_instance=RequestContext(request))


@login_required
def viewClass(request, class_id):
    c = get_object_or_404(Class, uid=class_id)
    if request.user == c.creator or request.user in c.teachers.all():
        return render_to_response("stu_response/class_view.html", {"class": c}, context_instance=RequestContext(request))
    elif request.user not in c.students.all():
        if request.method == "POST":
            form = ClassRegistrationForm(data=request.POST)
            if request.POST.get("password", False) and request.POST.get("password") == c.password:
                c.students.add(request.user)
                return redirect("/home/")
            else:
                form._errors = ErrorDict()
                form._errors['password'] = ErrorList([u"Invalid password. Please check your password and try again."])
        else:
            form = ClassRegistrationForm()
        return render_to_response("form_base.html", {"form": form, "submit_text": "Join Class", "form_title": c.name + " requires a password to join."}, context_instance=RequestContext(request))
    else:
        return render_to_response("stu_response/class_view.html", {"class": c}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def getResponses(request, lesson_id, q_num=None, stu_id=None):
    lesson = get_object_or_404(Lesson, key=lesson_id)

    lesson_is_in = lesson.class_set.all()
    user_is_legit = False
    for cls in lesson_is_in:
        if request.user in cls.teachers.all():
            user_is_legit = True
    if not user_is_legit:
        return HttpResponseForbidden("You do not have access to this page.")

    if request.GET.get("order", False) and request.GET.get("order") != "":
        responses = lesson.getResponses(stu_id=stu_id, q_num=q_num, order=request.GET.get("order"))
    else:
        responses = lesson.getResponses(stu_id=stu_id, q_num=q_num)
    response_set = []
    classes = None
    if request.GET.get("classes", False) and request.GET.get("classes") != "":
        classes = Class.objects.get(uid=request.GET.get("classes"))
    for x in responses:
        for r in x:
            curr = {
                "response": r.text,
                "edit_date": r.get_format_date(),
                "viewed": r.viewed,
                "student": r.student.get_full_name(),
                "q_num": r.question.q_num,
                "r_id": r.uid,
                "comment": r.comment,
            }
            if classes is not None and r.student in classes.students.all():
                response_set.append(curr)
            elif classes is None:
                response_set.append(curr)
    return HttpResponse(simplejson.dumps({"responses": response_set}), mimetype="application/json")


@user_passes_test(lambda u: u.is_staff)
def getStudentsInLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)

    lesson_is_in = lesson.class_set.all()
    user_is_legit = False
    for cls in lesson_is_in:
        if request.user in cls.teachers.all():
            user_is_legit = True
    if not user_is_legit:
        return HttpResponseForbidden("You do not have access to this page.")

    users = {
        "working": [],
        "seen": [],
        "completed": [],
    }
    temp = []
    for u in lesson.getStudentsCompleted():
        temp.append(u)
        curr = {
            "first": u.first_name,
            "last": u.last_name,
            "username": u.username,
        }
        users["completed"].append(curr)
    for u in lesson.getStudentsResponded():
        if u not in temp:
            curr = {
                "first": u.first_name,
                "last": u.last_name,
                "username": u.username,
            }
            if responsesAllViewed(user=u, lesson=lesson):
                users["seen"].append(curr)
            else:
                users["working"].append(curr)
    return HttpResponse(simplejson.dumps(users), mimetype='application/json')


@user_passes_test(lambda u: u.is_staff)
def toggleSeen(request, r_id):
    if request.is_ajax() and request.GET.get('seen', False) and request.user.is_staff:
        r = Response.objects.get(uid=r_id)

        lesson = r.question.lesson_set.all()[0]
        lesson_is_in = lesson.class_set.all()
        user_is_legit = False
        for cls in lesson_is_in:
            if request.user in cls.teachers.all():
                user_is_legit = True
        if not user_is_legit:
            return HttpResponseForbidden("You do not have access to this page.")

        r.viewed = True if request.GET['seen'] == '1' else False
        r.save()
        return HttpResponse(simplejson.dumps({"seen": r.viewed}), mimetype="application/json")
    return HttpResponseForbidden("You do not have the correct permissions to view this page")


def home(request, responses=False):
    lessons = []
    if request.user.is_authenticated():
        if responses:
            lesson_set = sorted(getRespondedLessons(request.user), key=lambda l: getPercentComplete(user=request.user, lesson=l))
            for l in lesson_set:
                curr = {
                    "lesson": l,
                    "completed": l.getNumCompleted(user_id=request.user.id),
                }
                lessons.append(curr)
            return render_to_response("user_home.html", {"lessons": lessons}, context_instance=RequestContext(request))
        if request.user.is_staff:
            classes = Class.objects.filter(teachers=request.user)
            lesson_set = [cls.lessons.select_related() for cls in classes]
            lesson_set = list(itertools.chain.from_iterable(lesson_set))
            lesson_set.sort(key=lambda l: l.id, reverse=True)
            for x in lesson_set:
                curr = {
                    "lesson": x,
                    "creator": x.creator,
                }
                lessons.append(curr)
            return render_to_response("staff_home.html", {"lessons": lessons}, context_instance=RequestContext(request))
        else:
            lesson_set = sorted(getRespondedLessons(request.user), key=lambda l: getPercentComplete(user=request.user, lesson=l))
            for l in lesson_set:
                curr = {
                    "lesson": l,
                    "completed": l.getNumCompleted(user_id=request.user.id),
                }
                lessons.append(curr)
        return render_to_response("user_home.html", {"lessons": lessons}, context_instance=RequestContext(request))
    return render_to_response("home.html", context_instance=RequestContext(request))
