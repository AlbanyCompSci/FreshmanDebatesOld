#!/usr/bin/env python3.4
#file: merge_debaters.py
#transform school-given student records to simple csv records for easy
#parsing into Django database

from tablib import Dataset

ENGLISH_COURSE_ID = "10CP01"
IHS_COURSE_ID     = "900012"
IN_FIELDS         = ['name', 'period', 'teacher', 'course_id']
OUT_FIELDS        = ['first_name', 'last_name', 'english_period',
                     'english_teacher', 'ihs_period', 'ihs_teacher']

#Dataset -> Dataset
def mergeDebaters(dataset):
    dataset.headers = IN_FIELDS
    debaters_old = dataset.dict
    english_debaters, ihs_debaters = [], []
    for d in debaters_old:
        if d['course_id'] == ENGLISH_COURSE_ID:
            english_debaters.append(d)
        elif d['course_id'] == IHS_COURSE_ID:
            ihs_debaters.append(d)
    dataset_new = Dataset()
    dataset_new.headers = OUT_FIELDS
    debaters_zipped = zipDebaters(english_debaters, ihs_debaters)
    debaters_zipped.reverse()
    for d in debaters_zipped:
        debater = splitName(d)
        #convert dictionary to a tuple and append it to the dataset
        l = []
        for key in OUT_FIELDS:
            l.append(debater[key])
        dataset_new.append(tuple(l))
    return dataset_new
    
def zipDebaters(english, ihs):
    if len(english) > 0:
        e = english[0]
        possible_is = []
        for d in ihs:
            if d['name'] == e['name']:
                possible_is.append(d)
        if len(ihs) > 0 and len(possible_is) > 0:
            i = possible_is[0]
            new_ihs = []
            for d in ihs:
                if d['name'] != e['name']:
                    new_ihs.append(d)
            new_debater = mergeDebater(e, i)
        else:
            new_debater = mergeDebater(e, None)
            new_ihs = ihs
    else:
        if len(ihs) > 0:
            new_debater = mergeDebater(None, ihs[0])
            new_ihs = ihs[1:]
        else:
            return []
    debaters = zipDebaters(english[1:], new_ihs)
    debaters.append(new_debater)
    return debaters

def mergeDebater(english, ihs):
    debater = {}
    if english != None:
        debater['name']            = english['name']
        debater['english_period']  = english['period']
        debater['english_teacher'] = english['teacher']
    else:
        debater['name']            = ""
        debater['english_period']  = ""
        debater['english_teacher'] = ""
    if ihs != None:
        debater['name']        = ihs['name']
        debater['ihs_period']  = ihs['period']
        debater['ihs_teacher'] = ihs['teacher']
    else:
        debater['ihs_period']  = ""
        debater['ihs_teacher'] = ""
    #if both english and ihs are null, return None
    if debater['name'] == "":
        return None
    #otherwise, return the constructed debater dict (may have None fields)
    return debater

def splitName(debater):
    name = debater['name']
    last_name  = name.split(", ")[0]
    first_name = name.split(", ")[1]
    debater.pop('name', None)
    debater['first_name'] = first_name
    debater['last_name']  = last_name
    return debater
