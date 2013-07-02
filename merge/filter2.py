#!/usr/bin/env python2
from DataDir import *
import itertools
import pdb,csv
import re

class Filter():
        """
                self.authors_pa : get the authors in PaperAuthor.csv
                self.authors_a : get the authors in Author.csv
                self.authors : self.authors_pa & self.authors_a
                self.authoraff : key: authorid, value : affiliation in the forms of words
                self.authorpapers : key: authorid, value: paperid set
                
        """
        def __init__(self):
                self.authors_pa=set()
                self.authors_a=set()
                self.authors=set()
                self.authoraff=dict()
                self.authorpapers=dict()
                self.paperauthors=dict()
                self.authorkeywords=dict()
                self.stopwords=set()
        def readfile(self):
                #import stopwords set
                with open(StopwordPath) as f:
                        for line in f:
                                self.stopwords.update(set(line.split()))
                print "Completed reading stopwords list!"
                with open(PaperAuthorPath) as csvfile:
                        reader=csv.reader(csvfile)
                        reader.next()
                        for row in reader:
                                self.authors_pa.add(row[1])
                #print "Completed reading PaperAuthor.csv!"
                with open(AuthorPath) as csvfile:
                        reader=csv.reader(csvfile)
                        reader.next()
                        for row in reader:
                                self.authors_a.add(row[0])
                self.authors=self.authors_pa & self.authors_a
                with open(PaperAuthorPath) as csvfile:
                        reader=csv.reader(csvfile)
                        reader.next()
                        for row in reader:
                                if row[1] in self.authors:
                                        # get co-author information
                                        if not self.authorpapers.has_key(row[1]):
                                                self.authorpapers[row[1]]=set()
                                        self.authorpapers[row[1]].add(row[0])
                                        if not self.paperauthors.has_key(row[0]):
                                                self.paperauthors[row[0]]=set()
                                        self.paperauthors[row[0]].add(row[1])
                # get affiliation information
                with open(AffilListPath) as csvfile :
                    reader = csv.reader(csvfile)
                    for row in reader :
                        if row[0] in self.authors :
                            longy = "|".join([row[1], row[2], row[3], row[4]])
                            longy = re.sub('\]','',longy)
                            longy = re.sub('\[','',longy)
                            aff_temp = [x.strip() for x in longy.split("|") if x.strip()!='']
                            aff = []
                            for item in aff_temp :
                                for sub in item.split():
                                    sub = sub.strip()
                                    if sub == 'ratory' or sub == 'rotory'or sub == 'ratoy' :
                                        sub = 'laboratory'
                                    if len(sub)>0 and sub[-1] == 's' :
                                        sub = sub[:-1]
                                    if sub not in aff :
                                        aff.append(sub)        
                            if len(aff)>0:
                                if not self.authoraff.has_key(row[0]):
                                    self.authoraff[row[0]]=set()
                                    self.authoraff[row[0]].update(set(aff)-self.stopwords)  # remove all the stopwords
                    
                print "Completed collecting affilation information !"
                with open(PaperPath) as csvfile:
                        reader=csv.reader(csvfile)
                        reader.next()
                        for row in reader:
                                if self.paperauthors.has_key(row[0]):
                                        # get keywords information
                                        keywords=set()
                                        row1=re.sub(r'[(),[]|\"]',' ',row[1])
                                        row1=re.sub('\]','',row1)
                                        row1=re.sub('\[','',row1)
                                        row1=row1.lower()
                                        key_temp = [x.strip() for x in row1.split("|") if x.strip()!='']
                                        _key = []
                                        for key in key_temp :
                                            for sub in key.split():
                                                if sub[-1] == 's' :
                                                    sub = sub[:-1]
                                                if sub not in _key :
                                                    _key.append(sub)
                                        keywords.update(set(_key))
                                        row5=re.sub(r'[(),[]\"]',' ',row[5])
                                        row5=re.sub('\]','',row5)
                                        row5=re.sub('\[','',row5)
                                        row5=row5.lower()

                                        key_temp = [x.strip() for x in row5.split("|") if x.strip()!='']
                                        _key = []
                                        for key in key_temp :
                                            for sub in key.split():
                                                if sub[-1] == 's' :
                                                    sub = sub[:-1]
                                                if sub not in _key :
                                                    _key.append(sub)
                                        keywords.update(set(_key))
                                        keywords=keywords-self.stopwords
                                        
                                        authors=list(self.paperauthors[row[0]])
                                        for i in range(len(authors)):
                                                if not self.authorkeywords.has_key(authors[i]):
                                                        self.authorkeywords[authors[i]]=set()
                                                self.authorkeywords[authors[i]].update(keywords)
                print "Completed collecting keyword information!"
        
        def query_aff(self,checkpair):
                Flag=0
                if self.authoraff.has_key(checkpair[0]) and self.authoraff.has_key(checkpair[1]):
                    length = len(self.authoraff[checkpair[0]] & self.authoraff[checkpair[1]]) > 0
                    if length > 0 :
                            Flag = length
                    else :
                            Flag = -1
                return Flag
        def query_keyword(self,checkpair):
                Flag = 0
                if self.authorkeywords.has_key(checkpair[0]) and self.authorkeywords.has_key(checkpair[1]):
                        len1 = len(self.authorkeywords[checkpair[0]])
                        len2 = len(self.authorkeywords[checkpair[1]])
                        length = len(self.authorkeywords[checkpair[0]] & self.authorkeywords[checkpair[1]]) 
                        if length > 0 :
                                Flag = length
                        else :
                                Flag = -1
                return Flag

def main():
        filter=Filter()
        filter.readfile()
        while True:
                checkpair=raw_input("Please Input 2 authors' id: ")
                checkpair=checkpair.split()
                print "------------------------------------------------------------------------------------------------"

                if filter.query_aff(checkpair) :
                        print "Affiliation True: ",filter.authoraff[checkpair[0]] & filter.authoraff[checkpair[1]]
                        print " "
                else :
                        print "Affiliation False: "
                        if filter.authoraff.has_key(checkpair[0]):
                                print checkpair[0]," : ",filter.authoraff[checkpair[0]]
                        if filter.authoraff.has_key(checkpair[1]):
                                print checkpair[1]," : ",filter.authoraff[checkpair[1]]
                        print " "

                if filter.query_keyword(checkpair) :
                        print "keyword True: ",filter.authorkeywords[checkpair[0]] & filter.authorkeywords[checkpair[1]]
                        print " "
                else :
                        print "keyword False: "
                        if filter.authorkeywords.has_key(checkpair[0]):
                                print checkpair[0],"        ",filter.authorkeywords[checkpair[0]]
                        if filter.authorkeywords.has_key(checkpair[1]):
                                print checkpair[1],"        ",filter.authorkeywords[checkpair[1]]
                        print " "


                pdb.set_trace()
                                
if __name__=="__main__":
        main()
