#!/usr/bin/env python3.4
#file resources.py

from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.instance_loaders import BaseInstanceLoader
from django.contrib.auth.models import Group, User
from debates.models import Debater, Teacher
from debates.merge_debaters import mergeDebaters
from logging import getLogger

logger = getLogger('logview.debugger')

class DebaterInstanceLoader(BaseInstanceLoader):
    def get_instance(self, row):
        debater = Debater()
        #TODO, change to email address
        full_name = str(row['first_name']) + " " + str(row['last_name'])
        logger.debug("Full name: " + full_name)
        debater.user = User.objects.create_user(full_name, password='')
        logger.debug("Username: " + str(debater.user.username))
        #debater.user.username = row['email']
        #debater.user.email = row['email']
        debater.user.first_name = row['first_name']
        debater.user.last_name = row['last_name']
        debaters_group = Group.objects.filter(name='debaters')
        debater.user.groups = [debaters_group]
        debater.user.is_staff = False
        english_teacher = list(Teacher.objects.filter(name=row['english_teacher']))[0]
        debater.english_teacher = english_teacher
        debater.english_period = int(str(row['english_period']))
        ihs_teacher = list(Teacher.objects.filter(name=row['ihs_teacher']))[0]
        debater.ihs_teacher = ihs_teacher
        debater.ihs_period = int(str(row['ihs_period']))
        return debater

class DebaterResource(ModelResource):
    #CSV Fields
    name      = Field(column_name='Student Name', readonly=True)
    period    = Field(column_name='Period', readonly=True)
    teacher   = Field(column_name='Teacher.', readonly=True)
    course_id = Field(column_name='Course.', readonly=True)
    
    def before_import(self, dataset, dry_run):
        #assignment of .dict needed to carry data over into calling function
        dataset.dict = mergeDebaters(dataset).dict

    class Meta(object):
        model = Debater
        #export_order = ('first_name','last_name',
        #                'english_period','english_teacher',
        #                'ihs_period','ihs_teacher')
        #import_id_fields = ['first_name', 'last_name']
        instance_loader_class = DebaterInstanceLoader

class TeacherResource(ModelResource):
    class Meta(object):
        model = Teacher
