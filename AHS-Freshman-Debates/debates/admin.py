#!/usr/bin/env python3.4
#file admin.py

from django.contrib.admin import autodiscover, site
from debates.models       import (
                                     Teacher, Judge, Debater,
                                     Topic, Location, Score, Subscore,
                                     Deduction, Debate, Team
                                 )
from debates.resources    import DebaterResource, TeacherResource
from import_export.admin  import ImportExportModelAdmin
#from logging              import getLogger

#logger = getLogger('logview.debugger')

autodiscover()

class DebaterAdmin(ImportExportModelAdmin):
    resource_class = DebaterResource

class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource

site.register(Teacher, TeacherAdmin)
site.register(Judge)
site.register(Debater, DebaterAdmin)
site.register(Topic)
site.register(Location)
site.register(Score)
site.register(Subscore)
site.register(Deduction)
site.register(Debate)
site.register(Team)#, TeamAdmin)
