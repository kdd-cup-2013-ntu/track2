#!/usr/bin/env python2
import csv
import re 

with open('buff/PAtoAa.csv','rb') as csvfile1 :
    creader1 = csv.reader(csvfile1)
    Name_map = {}
    Affil_map = {}
    for row in creader1 :
        row1 = row[1]
        row2 = row[2]
        Id = int(row[0])
        row1 = row1.replace('.','')
        row1 = row1.replace('-',' ')
        row1 = row1.lower()
        if Id in Name_map :
            same = 0
            for name in Name_map[Id] :
                if row1 == name :
                    same = 100
                    break 
            if same == 0 :
                Name_map[Id].append(row1)

            for affil in row2.split("|") :
                if affil !='':
                    have_same = 0
                    for aff in Affil_map[Id] :
                        if affil == aff :
                            have_same = 100
                            break
                    if have_same == 0 :
                        Affil_map[Id].append(affil)
        else :
            Name_map[Id] = [row1]
            Affil_map[Id] = []
            for affil in row2.split("|") :
                if affil !='' :
                    Affil_map[Id].append(affil)

    sorted_name = sorted(Name_map.iteritems())

with open('buff/PA_speci.csv','wb') as csvfile2 :
    cwriter = csv.writer(csvfile2)
    for item in sorted_name :
        Name = "|".join(str(x) for x in Name_map[int(item[0])])
        Affil = "|".join(str(x) for x in Affil_map[int(item[0])])
        cwriter.writerow([item[0],Name,Affil])


