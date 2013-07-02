#!/usr/bin/env python2
import csv
import operator
import re
with open('buff/Paper.TitleStat.csv') as csvfile2 :
    Max = 32000
    creader2 = csv.reader(csvfile2)
    Stat = {}
    for row in creader2 :
        Stat[row[1]] = int(row[0])
with open('data/Paper.csv','rb') as csvfile1:
    creader1 = csv.reader(csvfile1)
    file_list = []
    for row in creader1 :
        title = []
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
                                if sub_word2!='' and sub_word2 not in title :
                                    if Max > Stat[sub_word2] >1 : 
                                        title.append(sub_word2)
                               
                        else :
                          if sub_word!='' and sub_word[-1] == 's':
                              sub_word = sub_word[:-1]
                          if sub_word!='' and sub_word not in title :
                              if Max > Stat[sub_word] > 1 :
                                  title.append(sub_word)
                elif ',' in word :
                    for sub_word in word.split(",") : 
                        if sub_word!='' and sub_word[-1] == 's':
                            sub_word = sub_word[:-1]
                        if sub_word!='' and sub_word not in title :
                            if Max > Stat[sub_word] > 1 :
                                title.append(sub_word)
                   
                else :
                    word = re.sub('[^a-zA-Z0-9-]','', word)
                    if word!='' and word[-1] == 's':
                        word = word[:-1]
                    if word!='' and word not in title :
                        if Max > Stat[word] > 1:
                            title.append(word)
            title = " ".join([str(wordy) for wordy in title])
            keywords = []
            if len(row[5]) != 0 :
                start = 0
                if 'keywords:' in row[5].lower()[:9] :
                    start = 10
                elif 'key words:' in row[5].lower()[:10] :
                    start = 11
                elif 'keywords' in row[5].lower()[:8] :
                    start = 9
                elif 'key words' in row[5].lower()[:9] :
                    start = 10
                mark = 0
                if '|' in row[5]:
                    mark = '|'
                elif '; ' in row[5].replace(',',';'):
                    mark = '; '
                elif ';' in row[5].replace(',',';'):
                    mark = ';'
                elif '.' in row[5] :
                    mark = '.'
                if mark != 0 :
                    keywords = "|".join([str(x) for x in row[5][start:].replace(',',';').replace('"','').split(mark)])
                elif len(keywords)!=0 :
                    keywords = row[5]
                else :
                    keywords =''
            file_list.append((row[0],title,row[2],row[3],row[4],keywords))             

with open('buff/Paper.TitleCut.csv','wb') as f :
    cwriter = csv.writer(f)
    for item in file_list :
        cwriter.writerow(item)
