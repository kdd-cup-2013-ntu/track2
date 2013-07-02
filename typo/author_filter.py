#!/usr/bin/python
import re, sys

def author_name_filter(name):
#	.
	#name = re.sub(r'\.', r'\. ', name)
	name = re.sub(r'\.', r' ', name)
#	-
	name = re.sub(r'-', r' ', name)
#	@
	name = re.sub(r'@.*$', r'', name)
#	?
	name = re.sub(r'\?', r'', name)
#	'
	name = re.sub(r'\'', r'', name)

#	deal with latin characters
#	to A 
	name = re.sub(r'\xc3[\x80-\x85]', r'A', name)
	name = re.sub(r'\xc4[\x80\x82\x84]', r'A', name)
#	to AE 
	name = re.sub(r'\xc3\x86', r'AE', name)
#	to C 
	name = re.sub(r'\xc3\x87', r'C', name)
	name = re.sub(r'\xc4[\x86\x88\x8a\x8c]', r'C', name)
#	to D 
	name = re.sub(r'\xc3\x90', r'D', name)
	name = re.sub(r'\xc4[\x8e\x90]', r'D', name)
#	to E 
	name = re.sub(r'\xc3[\x88-\x8b]', r'E', name)
	name = re.sub(r'\xc4[\x92\x94\x96\x98\x9a]', r'E', name)
#	to G
	name = re.sub(r'\xc4[\x9c\x9e\xa0\xa2]', r'G', name)
#	to I 
	name = re.sub(r'\xc3[\x8c-\x8f]', r'I', name)
	name = re.sub(r'\xc4[\xa8\xaa\xac\xae\axb0]', r'I', name)
#	to J
	name = re.sub(r'\xc4\xb4', r'J', name)
#	to N 
	name = re.sub(r'\xc3\x91', r'N', name)
#	to O 
	name = re.sub(r'\xc3[\x92-\x96\x98]', r'O', name)
	name = re.sub(r'\xc5[\x8c\x8e\x90]', r'O', name)
#	to S
	name = re.sub(r'\xc5[\x9a\x9c\x9e\xa0]', r'S', name)
#	to U 
	name = re.sub(r'\xc3[\x99-\x9c]', r'U', name)
	name = re.sub(r'\xc5[\xa8\xaa\xac\xae\xb0]', r'U', name)
#	to Y 
	name = re.sub(r'\xc3\x9d', r'Y', name)
#	to Th 
	name = re.sub(r'\xc3\x9e', r'Th', name)
#	to s 
	name = re.sub(r'\xc3\x9f', r's', name)
#	to a 
	name = re.sub(r'\xc3[\xa0-\xa5]', r'a', name)
	name = re.sub(r'\xc4[\x81\x83\x85]', r'a', name)
#	to ae 
	name = re.sub(r'\xc3\xa6', r'ae', name)
#	to c 
	name = re.sub(r'\xc3\xa7', r'c', name)
	name = re.sub(r'\xc4[\x87\x89\x8b\x8d]', r'c', name)
#	to d
	name = re.sub(r'\xc3\xb0', r'd', name)
	name = re.sub(r'\xc4[\x8f\x91]', r'd', name)
#	to e 
	name = re.sub(r'\xc3[\xa8-\xab]', r'e', name)
	name = re.sub(r'\xc4[\x93\x95\x97\x99\x9b]', r'e', name)
	name = re.sub(r'\xc8\xa9', r'e', name)
#	to g
	name = re.sub(r'\xc4[\x9d\x9f\xa1\xa3]', r'g', name)
#	to i 
	name = re.sub(r'\xc3[\xac-\xaf]', r'i', name)
	name = re.sub(r'\xc4[\xa9\xab\xad\xaf\axb1]', r'i', name)
#	to j
	name = re.sub(r'\xc4\xb5', r'j', name)
#	to n 
	name = re.sub(r'\xc3\xb1', r'n', name)
#	to o 
	name = re.sub(r'\xc3[\xb2-\xb6\xb8]', r'o', name)
	name = re.sub(r'\xc5[\x8d\x8f\x91]', r'o', name)
#	to s
	name = re.sub(r'\xc5[\x9b\x9d\x9f\xa1]', r's', name)
#	to u 
	name = re.sub(r'\xc3[\xb9-\xbc]', r'u', name)
	name = re.sub(r'\xc5[\xa9\xab\xad\xaf\xb1]', r'u', name)
#	to y 
	name = re.sub(r'\xc3[\xbd\xbf]', r'y', name)
#	to th
	name = re.sub(r'\xc3\xbe', r'th', name)

#	to 

#	to L
	name = re.sub(r'\xc5\x82', r'L', name)
#	to l
	name = re.sub(r'\xc5\x91', r'l', name)

#	haven't done '\xce\xbe', '\xce\xbf', '\xcf\x80', '\xcf\x9a'

#	else
	name = re.sub(r'[^A-Za-z\(\)\s\?\.]', r'', name)
#	\s+
	name = re.sub(r'\s+', r' ', name)

	return name.lower()

if __name__=='__main__':
	print 'please type: '
	s = sys.stdin.readline()
	print author_name_filter(s.rstrip())
