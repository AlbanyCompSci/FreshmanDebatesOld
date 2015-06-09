from user_manage.models import InfoEditForm, RegistrationForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def editInfo(request, msg=""):
    if request.method == "POST":
        form = InfoEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'User information changed.')
            return redirect(request.POST.get("next"))
    else:
        form = InfoEditForm(instance=request.user)
    return render_to_response("usermanage/edit_info.html", {"form": form, "new_user": request.GET.get("nu", False), "next": request.GET.get("next", "/home/")}, context_instance=RequestContext(request))


def registerUser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/")
    else:
        form = RegistrationForm()
    return render_to_response("form_base.html", {"form": form, "submit_text": "Register", "form_title": "User Registration"})
