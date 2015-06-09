from django.contrib import admin
#from django.contrib.auth.models import User, Group

from api_app.models import Team, Debate, Score, Evaluation

admin.site.register(Team)
admin.site.register(Debate)
admin.site.register(Score)
admin.site.register(Evaluation)
