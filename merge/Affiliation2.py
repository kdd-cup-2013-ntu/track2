#!/usr/bin/env python
'''
In this file, we tried to seperate affiliation information into 4 categories: 

    University, Institute, Field, Other

The main reason for doing so is that we can avoid misleading matching by some of the information.

Ex. Author1, National Taiwan University | physic department | Address1
    Author2, Washington University | physic department | Address2

If we only calculate the number of matching words, we might recongnize these 2 people as the same person by the word "physic".
However, we didn't use the categories in the final submission. We simply concatenated all the information we have and put all the words into a set. So in this part, you can focus mainly on typo management.

'''

import csv
import re

with open('buff/PA_speci.csv','rb') as csvfile1 :
    creader1 = csv.reader(csvfile1)
    University = {}
    Inst = {}
    Field = {}
    Other = {}
    for row in creader1 :
        Id = int(row[0])
        row2 = row[2].lower()
        row2 = unicode(row2,"utf-8")
        row2 = row2.encode('ascii','ignore')
        row2 = re.sub(r'</?\w+[^>]*>',' ',row2)
        row2 = row2.replace(" .", ".")
        row2 = re.sub(' de ',' of ',row2)
        row2 = re.sub(' di ',' of ',row2)
        row2 = re.sub('univ ','university',row2)
        row2 = re.sub("univ.","university",row2)
        row2 = row2.replace("lab.","laboratoy")
        row2 = re.sub('laboratories','laboratoy',row2)
        row2 = re.sub('universite','university',row2)
        row2 = re.sub('universityrsidaof','university',row2)
        row2 = re.sub('universiteir ','university ',row2)
        row2 = re.sub('universityr','univer',row2)
        row2 = re.sub('universit ','university ',row2)
        row2 = re.sub('universityer','univer',row2)
        row2 = re.sub('universityrsit','university',row2)
        row2 = re.sub('universidade','university',row2)
        row2 = re.sub('universidaof','university',row2)
        row2 = re.sub('universidade de','university of',row2)
        row2 = re.sub('ofpartment',' department ',row2)
        row2 = re.sub('ofpartamento',' department ',row2)
        row2 = re.sub('ofpartmento',' department ',row2)
        row2 = row2.replace('ofpt.',' department ')
        row2 = re.sub('instituto','institute',row2)
        row2 = re.sub('institte','institute',row2)
        row2 = re.sub('institut','institute',row2)
        row2 = re.sub('institutee','institute',row2)
        row2 = row2.replace(" tech."," technology")
        row2 = row2.replace(" sci."," science")
        row2 = re.sub('centre','center',row2)
        row2 = re.sub(' fur ',' for ',row2)
        row2 = row2.replace('dept.','department')
        row2 = re.sub('dipartimento','department',row2)
        row2 = re.sub('department s of','department of',row2)
        row2 = re.sub('instituteof','institute of ',row2)
        row2 = re.sub('niversityof','niversity of ',row2)
        row2 = re.sub('university do','university of',row2)
        row2 = re.sub(r'([a-z0-9]+] {[a-z0-9]+} [[a-z0-9]+)','',row2)
        row2 = re.sub('institute of technology (?=([a-z0-9 .]+))','institue of technology|',row2)
        row2 = row2.replace('+','')
        row2 = re.sub('universite','university',row2)
        row2 = row2.replace('*','')
        row2 = row2.replace('&','and')
        row2 = row2.replace('#','and')
        row2 = row2.replace('%','')
        row2 = row2.replace('$','')
        row2 = row2.replace('^','')
        row2 = row2.replace('}','')
        row2 = row2.replace('{','')        
        row2 = row2.replace('/','')
        row2 = row2.replace('[','')
        row2 = row2.replace(']','')
        row2 = row2.replace(':',' ')
        row2 = row2.replace('?','')
        row2 = row2.replace('-',' ')
        row2 = row2.replace('\\','')
        row2 = re.sub("  "," ",row2)
        row2 = row2.replace(')','')
        row2 = row2.replace('(','')
        row2 = re.sub("   "," ",row2)
        row2 = re.sub("    "," ",row2)
        row2 = row2.replace(',','|')
        row2 = row2.replace(';','|')
        row2 = re.sub(r'university (?!of)',"university|",row2)
        row2 = re.sub(r'department (?!of)',"department|",row2)
        row2 = re.sub(r'department of',"|department of",row2)        
        _poss = row2.split("|")
        _University = []
        _Field = []
        _Inst = []
        _Other = []
        University[Id] = []
        Inst[Id] = []
        Field[Id] = []
        Other[Id] = []
        for item in _poss :
            sub_name = item
            sub_name = sub_name.strip()
            if 'university of ' in sub_name.lower() or ' university' in sub_name.lower() :
                if sub_name.lower() not in _University :
                    _University.append(sub_name.lower() )
        _University = sorted(_University,key = len)
        have2 = 0   
        have3 = 0
        have4 = 0
        if len(_University) > 3 :
            University[Id].append(_University[0])
            if _University[0] not in _University[1] :
                have2 = 100
                University[Id].append(_University[1])
            if _University[0] not in _University[2] and _University[1] not in _University[2] :
                have3 = 100
                University[Id].append(_University[2])
            if _University[0] not in _University[3] and _University[1] not in _University[3] and _University[2] not in _University[3] :
                have4 = 100
                University[Id].append(_University[3])
            for item in _University :
                if _University[0] not in item and (have2 == 0 or _University[1] not in item) and (have3 == 0 or _University[2] not in item) and (have4 == 0 or _University[3] not in item) :
                    University[Id].append(item)

        elif len(_University) > 2 :
            University[Id].append(_University[0])
            if _University[0] not in _University[1] :
                have2 = 100
                University[Id].append(_University[1])
            if _University[0] not in _University[2] and _University[1] not in _University[2] :
                have3 = 100
                University[Id].append(_University[2])
            for item in _University :
                if _University[0] not in item and (have2 == 0 or _University[1] not in item) and (have3 == 0 or _University[2] not in item):
                    University[Id].append(item)
        elif len(_University) > 1 :
            University[Id].append(_University[0])
            if _University[0] not in _University[1] :
                have2 = 100
                University[Id].append(_University[1])
            for item in _University :
                if _University[0] not in item and (have2 == 0 or _University[1] not in item):
                    University[Id].append(item)
        elif len(_University) == 1 :
            University[Id].append(_University[0])
            for item in _University :
                if item not in _University[0]:
                    University[Id].append(item)
        for uni in University[Id] :
            row2 = re.sub(uni,'',row2)
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if 'department of ' in sub_name or ' department' in sub_name.lower() or 'lab' in sub_name or 'school of' in sub_name.lower(): 
                    sub_name = re.sub('department of ','',sub_name)
                    sub_name = re.sub(' department','',sub_name)
                    sub_name = re.sub('lab([a-z]?)','',sub_name)
                    sub_name = re.sub('school of','',sub_name)
                    sub_name = sub_name.strip()
                    if sub_name.lower() not in _Field :
                        _Field.append(sub_name)

        _Field = sorted(_Field,key = len)
        have2 = 0
        have3 = 0
        have4 = 0
        have5 = 0

        if len(_Field) > 4 :
            Field[Id].append(_Field[0])
            if _Field[0] not in _Field[1] :
                have2 = 100
                Field[Id].append(_Field[1])
            if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                have3 = 100
                Field[Id].append(_Field[2])
            if _Field[0] not in _Field[3] and _Field[1] not in _Field[3] and _Field[2] not in _Field[3] :
                have4 = 100
                Field[Id].append(_Field[3])
            if _Field[0] not in _Field[4] and _Field[1] not in _Field[4] and _Field[2] not in _Field[4] and _Field[3] not in _Field[4] :
                have5 = 100
                Field[Id].append(_Field[4])
            for item in _Field :
                if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item) and (have4==0 or _Field[3] not in item) and (have5 == 0 or _Field[4] not in item) and item not in Field[Id]:
                    Field[Id].append(item)
        elif len(_Field) > 3 :
            Field[Id].append(_Field[0])
            if _Field[0] not in _Field[1] :
                have2 = 100
                Field[Id].append(_Field[1])
            if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                have3 = 100
                Field[Id].append(_Field[2])
            if _Field[0] not in _Field[3] and _Field[1] not in _Field[3] and _Field[2] not in _Field[3] :
                have4 = 100
                Field[Id].append(_Field[3])
            for item in _Field :
                if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item) and (have4==0 or _Field[3] not in item):
                    Field[Id].append(item)
        elif len(_Field) > 2 :
            Field[Id].append(_Field[0])
            if _Field[0] not in _Field[1] :
                have2 = 100
                Field[Id].append(_Field[1])
            if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                have3 = 100
                Field[Id].append(_Field[2])
            for item in _Field :
                if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item):
                    Field[Id].append(item)
        elif len(_Field) > 1 :
            Field[Id].append(_Field[0])
            if _Field[0] not in _Field[1] :
                have2 = 100
                Field[Id].append(_Field[1])
            for item in _Field :
                if _Field[0] not in item and (have2 == 0 or _Field[1] not in item):
                    Field[Id].append(item)
        elif len(_Field) == 1 :
            Field[Id].append(_Field[0])
            for item in _Field :
                if item not in _Field[0]:
                    Field[Id].append(item)
        for uni in Field[Id] :
            row2 = re.sub(uni,'',row2)
        
        row2 = re.sub('department of ','',row2)
        row2 = re.sub(' department','',row2)
        row2 = re.sub('lab([a-z]?)','',row2)
        row2 = re.sub('school of','',row2)
        row2 = row2.strip()
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if "institute " in sub_name  or 'center ' in sub_name or ' center' in sub_name or ' unit' in sub_name or 'centro ' in sub_name or ' group' in sub_name or 'research' in sub_name:
                    if sub_name not in _Inst and sub_name!='':
                        _Inst.append(sub_name )
        _Inst = sorted(_Inst,key = len)
        have2 = 0
        have3 = 0
        if len(_Inst) > 2 :
            Inst[Id].append(_Inst[0])
            if _Inst[0] not in _Inst[1] :
                have2 = 100
                Inst[Id].append(_Inst[1])
            if _Inst[0] not in _Inst[2] and _Inst[1] not in _Inst[2] :
                have3 = 100
                Inst[Id].append(_Inst[2])
            for item in _Inst :
                if _Inst[0] not in item and (have2 == 0 or _Inst[1] not in item) and (have3 == 0 or _Inst[2] not in item):
                    Inst[Id].append(item)
        elif len(_Inst) > 1 :
            Inst[Id].append(_Inst[0])
            if _Inst[0] not in _Inst[1] :
                have2 = 100
                Inst[Id].append(_Inst[1])
            for item in _Inst :
                if item not in Inst[Id] and _Inst[0] not in item and (have2 == 0 or _Inst[1] not in item):
                    Inst[Id].append(item)
        elif len(_Inst) == 1 :
            Inst[Id].append(_Inst[0])
            for item in _Inst :
                if item not in _Inst[0]:
                    Inst[Id].append(item)
        for uni in Inst[Id] :
            row2 = re.sub(uni,'',row2.lower())
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if sub_name != '':
                    if sub_name.lower() not in _Other :
                       _Other.append(sub_name.lower())
        _Other = sorted(_Other,key = len)
        Other_temp = []
        for item1 in _Other :
            item1 = item1.strip()
            if item1!='':
                Other_temp.append(item1)
                item1 = " "+item1 + " "
                for id,item2 in enumerate (_Other) :
                    item2 = " "+item2 + " "
                    if item1 in item2 :
                        _Other[id] = item2.replace(str(item1),"")
        for select in Other_temp :
            select = select.strip()
            if select != '' and select not in Other[Id]:
                Other[Id].append(select)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

with open('data/Author.csv','rb') as csvfile2 :
    creader2 = csv.reader(csvfile2)
    for row in creader2 :
        if creader2.line_num == 1 :
            continue
        Id = int(row[0])
        row2 = row[2].lower()
        row2 = unicode(row2,"utf-8")
        row2 = row2.encode('ascii','ignore')
        row2 = re.sub(r'</?\w+[^>]*>',' ',row2)
        row2 = row2.replace(" .", ".")
        row2 = re.sub(' de ',' of ',row2)
        row2 = re.sub(' di ',' of ',row2)
        row2 = re.sub('univ ','university',row2)
        row2 = re.sub('univ.','university',row2)
        row2 = re.sub("lab.","laboratory ",row2)
        row2 = re.sub('laboratories','laboratory',row2)
        row2 = re.sub('universite','university',row2)
        row2 = re.sub('universityrsidaof','university',row2)
        row2 = re.sub('universiteir ','university ',row2)
        row2 = re.sub('universityr','univer',row2)
        row2 = re.sub('universit ','university ',row2)
        row2 = re.sub('universityer','univer',row2)
        row2 = re.sub('universityrsit','university',row2)
        row2 = re.sub('universidade','university',row2)
        row2 = re.sub('universidaof','university',row2)
        row2 = re.sub('universidade de','university of',row2)
        row2 = re.sub('ofpartment',' department ',row2)
        row2 = re.sub('ofpartamento',' department ',row2)
        row2 = re.sub('ofpartmento',' department ',row2)
        row2 = re.sub('ofpt.',' department ',row2)
        row2 = re.sub('instituto','institute',row2)
        row2 = re.sub('institte','institute',row2)
        row2 = re.sub('institut','institute',row2)
        row2 = re.sub('institutee','institute',row2)
        row2 = re.sub('centre','center',row2)
        row2 = re.sub(' fur ',' for ',row2)
        row2 = re.sub('dept.','department of',row2)
        row2 = re.sub('dipartimento','department',row2)
        row2 = re.sub('department s of','department of',row2)
        row2 = re.sub('instituteof','institute of ',row2)
        row2 = re.sub('niversityof','niversity of ',row2)
        row2 = re.sub('university do','university of',row2)
        row2 = re.sub(r'([a-z0-9]+] {[a-z0-9]+} [[a-z0-9]+)','',row2)
        row2 = row2.replace('+','')
        row2 = re.sub('universite','university',row2)
        row2 = row2.replace('*','')
        row2 = row2.replace('&','and')
        row2 = row2.replace('#','and')
        row2 = row2.replace('%','')
        row2 = row2.replace('$','')
        row2 = row2.replace('^','')
        row2 = row2.replace('}','')
        row2 = row2.replace('{','')        
        row2 = row2.replace('/','')
        row2 = row2.replace('[','')
        row2 = row2.replace(']','')
        row2 = row2.replace(':',' ')
        row2 = row2.replace('?','')
        row2 = row2.replace('-',' ')
        row2 = row2.replace('\\','')
        row2 = re.sub("  "," ",row2)
        row2 = row2.replace(')','')
        row2 = row2.replace('(','')
        row2 = re.sub("   "," ",row2)
        row2 = re.sub("    "," ",row2)
        row2 = row2.replace(',','|')
        row2 = row2.replace(';','|')
        _poss = row2.split("|")
        inPA = 100
        if Id not in University :
            inPA = 0
            _University = []
            _Field = []
            _Inst = []
            _Other = []
            University[Id] = []
            Inst[Id] = []
            Field[Id] = []
            Other[Id] = []
        for item in _poss :
            # possName = item.split(',')
            sub_name = item
            sub_name = sub_name.strip()
            if 'university of ' in sub_name or ' university' in sub_name :
                if inPA == 0 :
                    if sub_name not in _University :
                        _University.append(sub_name)
                else :
                    if sub_name not in University[Id] :
                        University[Id].append(sub_name)
        if inPA == 0 :
            _University = sorted(_University,key = len)
            have2 = 0   
            have3 = 0
            have4 = 0
            if len(_University) > 3 :
                University[Id].append(_University[0])
                if _University[0] not in _University[1] :
                    have2 = 100
                    University[Id].append(_University[1])
                if _University[0] not in _University[2] and _University[1] not in _University[2] :
                    have3 = 100
                    University[Id].append(_University[2])
                if _University[0] not in _University[3] and _University[1] not in _University[3] and _University[2] not in _University[3] :
                    have4 = 100
                    University[Id].append(_University[3])
                for item in _University :
                    if _University[0] not in item and (have2 == 0 or _University[1] not in item) and (have3 == 0 or _University[2] not in item) and (have4 == 0 or _University[3] not in item) :
                        University[Id].append(item)

            elif len(_University) > 2 :
                University[Id].append(_University[0])
                if _University[0] not in _University[1] :
                    have2 = 100
                    University[Id].append(_University[1])
                if _University[0] not in _University[2] and _University[1] not in _University[2] :
                    have3 = 100
                    University[Id].append(_University[2])
                for item in _University :
                    if _University[0] not in item and (have2 == 0 or _University[1] not in item) and (have3 == 0 or _University[2] not in item):
                        University[Id].append(item)
            elif len(_University) > 1 :
                University[Id].append(_University[0])
                if _University[0] not in _University[1] :
                    have2 = 100
                    University[Id].append(_University[1])
                for item in _University :
                    if _University[0] not in item and (have2 == 0 or _University[1] not in item):
                        University[Id].append(item)
            elif len(_University) == 1 :
                University[Id].append(_University[0])
                for item in _University :
                    if item not in _University[0]:
                        University[Id].append(item)
        for uni in University[Id] :
            row2 = re.sub(uni,'',row2)
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if 'department of ' in sub_name or ' department' in sub_name.lower() or 'lab' in sub_name or 'school of' in sub_name.lower():
                    if inPA == 0 :
                        sub_name = re.sub('department of ','',sub_name)
                        sub_name = re.sub(' department','',sub_name)
                        sub_name = re.sub('lab([a-z]?)','',sub_name)
                        sub_name = re.sub('school of','',sub_name)
                        sub_name = sub_name.strip()
                        if sub_name not in _Field :
                            _Field.append(sub_name)
                         
                    else :
                        sub_name = re.sub('department of ','',sub_name)
                        sub_name = re.sub(' department','',sub_name)
                        sub_name = re.sub('lab([a-z]?)','',sub_name)
                        sub_name = re.sub('school of','',sub_name)
                        sub_name = sub_name.strip()
                        if sub_name not in Field[Id] :
                            Field[Id].append(sub_name)
        if inPA == 0 :
            _Field = sorted(_Field,key = len)
            have2 = 0
            have3 = 0
            have4 = 0
            have5 = 0

            if len(_Field) > 4 :
                Field[Id].append(_Field[0])
                if _Field[0] not in _Field[1] :
                    have2 = 100
                    Field[Id].append(_Field[1])
                if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                    have3 = 100
                    Field[Id].append(_Field[2])
                if _Field[0] not in _Field[3] and _Field[1] not in _Field[3] and _Field[2] not in _Field[3] :
                    have4 = 100
                    Field[Id].append(_Field[3])
                if _Field[0] not in _Field[4] and _Field[1] not in _Field[4] and _Field[2] not in _Field[4] and _Field[3] not in _Field[4] :
                    have5 = 100
                    Field[Id].append(_Field[4])
                for item in _Field :
                    if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item) and (have4==0 or _Field[3] not in item) and (have5 == 0 or _Field[4] not in item) and item not in Field[Id]:
                        Field[Id].append(item)
            elif len(_Field) > 3 :
                Field[Id].append(_Field[0])
                if _Field[0] not in _Field[1] :
                    have2 = 100
                    Field[Id].append(_Field[1])
                if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                    have3 = 100
                    Field[Id].append(_Field[2])
                if _Field[0] not in _Field[3] and _Field[1] not in _Field[3] and _Field[2] not in _Field[3] :
                    have4 = 100
                    Field[Id].append(_Field[3])
                for item in _Field :
                    if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item) and (have4==0 or _Field[3] not in item):
                        Field[Id].append(item)
            elif len(_Field) > 2 :
                Field[Id].append(_Field[0])
                if _Field[0] not in _Field[1] :
                    have2 = 100
                    Field[Id].append(_Field[1])
                if _Field[0] not in _Field[2] and _Field[1] not in _Field[2] :
                    have3 = 100
                    Field[Id].append(_Field[2])
                for item in _Field :
                    if _Field[0] not in item and (have2 == 0 or _Field[1] not in item) and (have3 == 0 or _Field[2] not in item):
                        Field[Id].append(item)
            elif len(_Field) > 1 :
                Field[Id].append(_Field[0])
                if _Field[0] not in _Field[1] :
                    have2 = 100
                    Field[Id].append(_Field[1])
                for item in _Field :
                    if _Field[0] not in item and (have2 == 0 or _Field[1] not in item):
                        Field[Id].append(item)
            elif len(_Field) == 1 :
                Field[Id].append(_Field[0])
                for item in _Field :
                    if item not in _Field[0]:
                        Field[Id].append(item)
        for uni in Field[Id] :
            row2 = re.sub(uni,'',row2)
        row2 = re.sub('department of ','',row2)
        row2 = re.sub(' department','',row2)
        row2 = re.sub('lab([a-z]?)','',row2)
        row2 = re.sub('school of','',row2)
        row2 = row2.strip()
           
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if "institute" in sub_name  or 'center ' in sub_name or ' center' in sub_name or ' unit' in sub_name or 'centro ' in sub_name or 'group' in sub_name or 'research' in sub_name:
                    if inPA == 0 :
                        if sub_name not in _Inst and sub_name!='':
                            _Inst.append(sub_name )
                    else :
                         if sub_name not in Inst[Id] :
                            Inst[Id].append(sub_name)
        if inPA == 0 :
            _Inst = sorted(_Inst,key = len)
            have2 = 0
            have3 = 0
            if len(_Inst) > 2 :
                Inst[Id].append(_Inst[0])
                if _Inst[0] not in _Inst[1] :
                    have2 = 100
                    Inst[Id].append(_Inst[1])
                if _Inst[0] not in _Inst[2] and _Inst[1] not in _Inst[2] :
                    have3 = 100
                    Inst[Id].append(_Inst[2])
                for item in _Inst :
                    if _Inst[0] not in item and (have2 == 0 or _Inst[1] not in item) and (have3 == 0 or _Inst[2] not in item):
                        Inst[Id].append(item)
            elif len(_Inst) > 1 :
                Inst[Id].append(_Inst[0])
                if _Inst[0] not in _Inst[1] :
                    have2 = 100
                    Inst[Id].append(_Inst[1])
                for item in _Inst :
                    if item not in Inst[Id] and _Inst[0] not in item and (have2 == 0 or _Inst[1] not in item):
                        Inst[Id].append(item)
            elif len(_Inst) == 1 :
                Inst[Id].append(_Inst[0])
                for item in _Inst :
                    if item not in _Inst[0]:
                        Inst[Id].append(item)
        for uni in Inst[Id] :
            row2 = re.sub(uni,'',row2.lower())
        _poss = row2.split('|')
        for item in _poss :
            possName = item.split(',')
            for sub_name in possName :
                sub_name = sub_name.strip()
                if sub_name != '':
                    if inPA == 0 :
                        if sub_name not in _Other :
                            _Other.append(sub_name.lower())
                    else :
                        if sub_name not in Other[Id] :
                            Other[Id].append(sub_name)
        if inPA == 0 :
            _Other = sorted(_Other,key = len)
            Other_temp = []
            for item1 in _Other :
                item1 = item1.strip()
                if item1!='':
                    Other_temp.append(item1)
                    item1 = " "+item1 + " "
                    for id,item2 in enumerate (_Other) :
                        item2 = " "+item2 + " "
                        if item1 in item2 :
                            _Other[id] = item2.replace(str(item1),"")
            for select in Other_temp :
                select = select.strip()
                if select != '' and select not in Other[Id]:
                    Other[Id].append(select)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

with open('buff/AffilList2.csv','wb') as csvfile3 :
    cwriter = csv.writer(csvfile3) 
    for item in University :
        cwriter.writerow([item,"|".join(University[item]),"|".join(Inst[item]),"|".join(Field[item]),"|".join(Other[item])])        
        
