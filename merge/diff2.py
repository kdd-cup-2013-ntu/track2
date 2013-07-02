#!/usr/bin/env python2
import csv
from filter2 import Filter

with open('buff/main1.csv','rb') as csvfile1 :
    creader1 = csv.reader(csvfile1)
    dic1 = {}
    for row in creader1 :
        if creader1.line_num == 1 :
            continue
        Id = int(row[0])
        dic1[Id] = [int(x) for x in row[1].split(" ")]

with open('buff/main2.csv','rb') as csvfile2 :
    creader2 = csv.reader(csvfile2)
    dic2 = {}
    for row in creader2 :
        if creader2.line_num == 1 :
            continue
        Id = int(row[0])        
        dic2[Id] = [int(x) for x in row[1].split(" ")]

filter = Filter()
filter.readfile()

dealed = {}
for item in dic1 :
    dealed[item] = []
    for kid in dic2[item]:
        if kid not in dic1[item]:
            i = item
            j = kid
            checkpair = [str(i)]
            checkpair.append(str(j))
                    
            Aff = filter.query_aff(checkpair) 
            Key = filter.query_keyword(checkpair) 
                    
            if ((Aff > 1 and Key > 0) or (Aff == 0 and Key > 1)) and (Key <= 75):
                dealed[i].append(j)

with open('buff/elite.csv','wb') as csvfile :
    cwriter = csv.writer(csvfile)
    for item in dealed :
        if len(dealed[item]) > 0 :
            cwriter.writerow([item, " ".join([str(x) for x in dealed[item]])])
