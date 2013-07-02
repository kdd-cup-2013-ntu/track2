# Copyright 2008, Jeffrey Regier, jeff [at] stat [dot] berkeley [dot] edu

# This file is part of Author-Dedupe.
#
# Author-Dedupe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Author-Dedupe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Author-Dedupe.  If not, see <http://www.gnu.org/licenses/>.

# The `replace_nickname()' function was added by Felix Wu on 2013/6/2

nick_names = {
    "al": "albert",
    "andy": "andrew",
    "tony": "anthony",
    "art": "arthur",
    "arty": "arthur",
    "bernie": "bernard",
    "bern": "bernard",
    "charlie": "charles",
    "chuck": "charles",
    "danny": "daniel",
    "dan": "daniel",
    "don": "donald",
    "ed": "edward",
    "eddie": "edward",
    "gene": "eugene",
    "fran": "francis",
    "freddy": "frederick",
    "fred": "frederick",
    "hank": "henry",
    "irv": "irving",
    "jimmy": "james",
    "jim": "james",
    "joe": "joseph",
    "jacky": "john",
    "jack": "john",
    "jeff": "jeffrey",
    "ken": "kenneth",
    "larry": "lawrence",
    "leo": "leonard",
    "matt": "matthew",
    "mike": "michael",
    "nate": "nathan",
    "nat": "nathan",
    "nick": "nicholas",
    "pat": "patrick",
    "pete": "peter",
    "ray": "raymond",
    "dick": "richard",
    "rick": "richard",
    "bob: bobby: rob": "robert",
    "ron: ronny": "ronald",
    "russ": "russell",
    "sam: sammy": "samuel",
    "steve": "stephan",
    "stu": "stuart",
    "teddy": "theodore",
    "ted": "theodore",
    "tom": "thomas",
    "thom": "thomas",
    "tommy": "thomas",
    "timmy": "timothy",
    "tim": "timothy",
    "walt": "walter",
    "wally": "walter",
    "bill": "william",
    "billy": "william",
    "will": "william",
    "willy": "william",
    "mandy": "amanda",
    "cathy": "catherine",
    "cath": "catherine",
    "chris": "christopher",
    "chrissy": "christine",
    "cindy: cynth": "cynthia",
    "debbie": "deborah",
    "deb": "deborah",
    "betty": "elizabeth",
    "beth": "elizabeth",
    "liz": "elizabeth",
    "bess": "elizabeth",
    "flo": "florence",
    "francie": "frances",
    "fran": "frances",
    "jan": "janet",
    "kate": "katherine",
    "kathy": "katherine",
    "jan": "janice",
    "nan": "nancy",
    "pam": "pamela",
    "pat": "patricia",
    "bobbie": "roberta",
    "sophie": "sophia",
    "sue": "susan",
    "suzie": "susan",
    "terry": "teresa",
    "val": "valerie",
    "ronnie": "veronica",
    "vonna": "yvonne",
}

def replace_nickname(name):
	name_split = name.split()
	new_name = list()
	for word in name_split:
		if word in nick_names:
			new_name.append(nick_names[word])
		else:
			new_name.append(word)
	return ' '.join(new_name)
