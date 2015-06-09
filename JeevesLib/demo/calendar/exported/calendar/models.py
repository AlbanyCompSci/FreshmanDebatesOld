
from django.db.models import CharField, DateTimeField
from jeevesdb.JeevesModel import JeevesModel as Model, JeevesForeignKey as ForeignKey
from jeevesdb.JeevesModel import label_for
from sourcetrans.macro_module import macros
import JeevesLib

class UserProfile(Model):
    username = CharField(max_length=256)
    email = CharField(max_length=256)

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
    def has_event(self):
        sym5 = JeevesLib.Namespace({'self':self}, 'has_event')
        sym5.sym3 = True
        sym5.sym4 = None
        pass
        return sym5.sym4

class Event(Model):
    name = CharField(max_length=256)
    location = CharField(max_length=512)
    time = DateTimeField()
    description = CharField(max_length=1024)

    @JeevesLib.supports_jeeves
    def has_host(self, host):
        sym8 = JeevesLib.Namespace({'self':self, 'host':host}, 'has_host')
        sym8.sym6 = True
        sym8.sym7 = None
        sym8.sym7 = (JeevesLib.jfun(EventHost.objects.get, host=sym8.host) != None)
        sym8.sym6 = False
        return sym8.sym7

    @JeevesLib.supports_jeeves
    def has_guest(self, guest):
        sym11 = JeevesLib.Namespace({'self':self, 'guest':guest}, 'has_guest')
        sym11.sym9 = True
        sym11.sym10 = None
        sym11.sym10 = (JeevesLib.jfun(EventGuest.objects.get, guest=sym11.guest) != None)
        sym11.sym9 = False
        return sym11.sym10

class EventHost(Model):
    'Relates events to hosts.\n    '
    event = ForeignKey(Event, null=True)
    host = ForeignKey(UserProfile, null=True)

class EventGuest(Model):
    'Relates events to guests.\n    '
    event = ForeignKey(Event, null=True)
    guest = ForeignKey(UserProfile, null=True)