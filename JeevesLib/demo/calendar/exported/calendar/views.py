
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from models import UserProfile
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
    real_view_fn.__name__ = view_fn.__name__
    return real_view_fn

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def index(request, user_profile):
    sym5 = JeevesLib.Namespace({'request':request, 'user_profile':user_profile}, 'index')
    sym5.sym3 = True
    sym5.sym4 = None
    sym5.sym4 = ('index.html', {'name':sym5.user_profile.email})
    sym5.sym3 = False
    return sym5.sym4

@login_required
@request_wrapper
@JeevesLib.supports_jeeves
def profile_view(request):
    sym8 = JeevesLib.Namespace({'request':request}, 'profile_view')
    sym8.sym6 = True
    sym8.sym7 = None
    sym8.profile = JeevesLib.jfun(UserProfile.objects.get, username=sym8.request.user.username)

    def sym9():
        sym8.profile = JeevesLib.jfun(UserProfile, username=sym8.request.user.username)

    def sym10():
        pass
    JeevesLib.jif((sym8.profile == None), sym9, sym10)

    def sym11():

        def sym13():
            sym8.profile.email = JeevesLib.jfun(sym8.request.POST.get, 'email', '')
            JeevesLib.jfun(sym8.profile.save)

        def sym14():
            pass
        JeevesLib.jif((sym8.request.method == 'POST'), sym13, sym14)

        def sym15():
            sym8.sym7 = ('profile.html', {'email':sym8.profile.email, 'which_page':'profile'})
            sym8.sym6 = False

        def sym16():
            pass
        JeevesLib.jif(sym8.sym6, sym15, sym16)

    def sym12():
        pass
    JeevesLib.jif(sym8.sym6, sym11, sym12)
    return sym8.sym7

def register_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('index')
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            UserProfile.objects.create(username=user.username, email=request.POST.get('email', ''))
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('index')
    else:
        form = UserCreationForm()
    return render_to_response('registration/account.html', RequestContext(request, {'form':form, 'which_page':'register'}))