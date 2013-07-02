#!/usr/bin/env python2
import csv
import operator
import re
with open('data/Paper.csv','rb') as csvfile1:
    creader1 = csv.reader(csvfile1)
    Stat = {}
    for row in creader1 :
        if creader1.line_num == 1 :
            continue
        else :        
            for word in row[1].lower().split(" ") :
                word = re.sub(r'</?\w+[^>]*>',' ',word)
                word = word.replace('"','')
                if '/' in word :
                    for sub_word in word.split("/") :       
                        if ',' in sub_word :
                            for sub_word2 in sub_word.split(",") :
                                if sub_word2!='' and sub_word2[-1] == 's':
                                    sub_word2 = sub_word2[:-1]
                                if sub_word2!='' and sub_word2 not in Stat :
                                    Stat[sub_word2] = 1
                                elif sub_word2 != '' :
                                    Stat[sub_word2] += 1
                               
                        else :
                          if sub_word!='' and sub_word[-1] == 's':
                              sub_word = sub_word[:-1]
                          if sub_word!='' and sub_word not in Stat :
                              Stat[sub_word] = 1
                          elif sub_word != '' :
                              Stat[sub_word] += 1
                elif ',' in word :
                    for sub_word in word.split(",") : 
                        if sub_word!='' and sub_word[-1] == 's':
                            sub_word = sub_word[:-1]
                        if sub_word!='' and sub_word not in Stat :
                            Stat[sub_word] = 1
                        elif sub_word != '' :
                            Stat[sub_word] += 1
                   
                else :
                    word = re.sub('[^a-zA-Z0-9-]','', word)
                    if word!='' and word[-1] == 's':
                        word = word[:-1]
                    if word!='' and word not in Stat :
                        Stat[word] = 1
                    elif word != '' :
                        Stat[word] += 1
   
    Sorted_stat = sorted(Stat.iteritems(), key = operator.itemgetter(1))

with open('buff/Paper.TitleStat.csv','wb') as f :
    cwriter = csv.writer(f)
    for word,num in Sorted_stat :
        cwriter.writerow([num,word])
