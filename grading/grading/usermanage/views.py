from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from usermanage.models import SchoolClass

def login(request):
    if request.user.is_authenticated():
        return redirect('/lessons/')
    else:
        return render(request, 'login.html', {})


@staff_member_required
def class_config(request):
    classes = request.user.teachers.select_related()
    return render(request, 'classes_overview.html', {
        'classes': classes,
    })


@staff_member_required
def new_class(request):
    if request.method == 'POST':
        teachers = [User.objects.get(id=i) for i in request.POST.getlist('teachers')]
        new_class = SchoolClass(
            name=request.POST['class_name'],
            password=request.POST['pssdwd']
        )
        new_class.save()
        new_class.teachers.add(*teachers)
        new_class.save()
        return redirect('/')
    teachers = User.objects.filter(Q(is_staff=True))
    return render(request, 'new_class.html', {
        'teachers': teachers,
    })


@login_required
def join_class(request, id):
    school_class = SchoolClass.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'join_class.html', {'school_class': school_class})
    elif request.method == 'POST' and request.POST['class_pwd'] == school_class.password:
        school_class.students.add(request.user)
        school_class.save()
        return redirect('/')
    else:
        return render(request, 'join_class.html', {'school_class': school_class,
                                                   'failed': True})
