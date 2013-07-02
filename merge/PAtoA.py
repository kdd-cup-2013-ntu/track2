#!/usr/bin/env python2
import csv

with open('data/Author.csv', 'rb') as csvfile :
    creader = csv.reader(csvfile)
    idList = set()
    for row in creader :
        if creader.line_num == 1:
            continue
        else :
            idList.add( int(row[0]) )

with open('data/PaperAuthor.csv' , 'rb') as csvfile1 :
    with open('buff/PAtoAa.csv' , 'wb') as csvfile2 : 
        cwriter = csv.writer(csvfile2)
        creader1 = csv.reader(csvfile1)
        NameMap = {}
        for row in creader1 :
            if creader1.line_num == 1 :
                continue
            else :
               if int(row[1]) in idList :
                   cwriter.writerow([row[1],row[2],row[3]])
