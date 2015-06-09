#!/usr/bin/env python3.4

from apiclient import

def populateUser(user_id):
    name = getUsername(user_id)
    school_info = getSchoolInfo(name)
    mkUser(dict({'name': name}.items() + school_info()))

def getUsername(user_id):
