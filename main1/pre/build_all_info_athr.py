#!/usr/bin/env python3
import sys, csv,collections
import pickle, copy

athr_basic_info_dic = collections.defaultdict(dict)
paper_basic_info_dic = {}
paper_athr_list_dic = {}
athr_full_info_dic = collections.defaultdict(dict)
cn_name_dic ={}
aids = []


def gen_athr_basic_info(author_f_name):
	global athr_basic_info_dic

	for aid, aname, aff in csv.reader(open(author_f_name, 'r', encoding='utf-8')):
		aid_post = int(aid)
		athr_basic_info_dic[aid_post]['name'] = aname
		athr_basic_info_dic[aid_post]['aff'] = aff

def gen_paper_basic_info(paper_f_name):
	global paper_basic_info_dic

	for p_id, p_ttl, p_yr, p_cf_id, p_jr_id, p_keys in csv.reader(open(paper_f_name, 'r',encoding='utf-8')):
		p_id_post = int(p_id)
		p_cf_id_post = int(p_cf_id)
		p_jr_id_post = int(p_jr_id)
		p_yr_post = int(p_yr)
		paper_basic_info_dic[p_id_post] = {} 
		paper_basic_info_dic[p_id_post]['title'] = p_ttl
#		paper_basic_info_dic[p_id_post]['year'] = p_yr_post
		paper_basic_info_dic[p_id_post]['con_id'] = p_cf_id_post
		paper_basic_info_dic[p_id_post]['jr_id'] = p_jr_id_post
		#paper_basic_info_dic[p_id_post]['keys'] = p_keys

def gen_cn_name_index(cn_name_f_name):
    global cn_name_dic

    for line in open(cn_name_f_name, 'r'):
        line_split = line.split(',')
        aid = int(line_split[0])
        cn_name_dic[aid] = 1

def gen_athr_full_dic(paper_author_f_name):
	global athr_full_info_dic
	global paper_athr_list_dic

	for pid, aid, aname, aff in csv.reader(open(paper_author_f_name, 'r', encoding='utf-8')):
		pid = int(pid)
		aid = int(aid)
		# Generate paper-athr list:  PaperID is written by AuthorID1, AuthorID2.....
		if pid not in paper_athr_list_dic:
			paper_athr_list_dic[pid] = [aid]
		else:
			paper_athr_list_dic[pid].append(aid)

		if aid not in athr_basic_info_dic: continue
		if aid not in athr_full_info_dic:
			athr_full_info_dic[aid]['name'] = athr_basic_info_dic[aid]['name']
			athr_full_info_dic[aid]['aliases'] = [athr_basic_info_dic[aid]['name']]
			if athr_basic_info_dic[aid]['aff'] != '':
				athr_full_info_dic[aid]['affs'] = [athr_basic_info_dic[aid]['aff']]
			else:
				athr_full_info_dic[aid]['affs'] = []
			athr_full_info_dic[aid]['pids'] = []
			athr_full_info_dic[aid]['con_ids'] = []
			athr_full_info_dic[aid]['jr_ids'] = []

			if aid in cn_name_dic:
				athr_full_info_dic[aid]['is_cn'] = True
			else:
				athr_full_info_dic[aid]['is_cn'] = False
#			athr_full_info_dic[aid]['years'] = []


		if aname != '':
			athr_full_info_dic[aid]['aliases'].append(aname)
		if aff != '':
			athr_full_info_dic[aid]['affs'].append(aff)

		athr_full_info_dic[aid]['pids'].append(pid)

		if pid in paper_basic_info_dic:
			if paper_basic_info_dic[pid]['con_id'] > 0: 
				athr_full_info_dic[aid]['con_ids'].append(paper_basic_info_dic[pid]['con_id'])
			if paper_basic_info_dic[pid]['jr_id'] > 0: 
				athr_full_info_dic[aid]['jr_ids'].append(paper_basic_info_dic[pid]['jr_id'])
#			athr_full_info_dic[aid]['years'].append(paper_basic_info_dic[pid]['year'])
#		else:
#			athr_full_info_dic[aid]['con_ids'].append(-2)
#			athr_full_info_dic[aid]['jr_ids'].append(-2)
#			athr_full_info_dic[aid]['years'].append(-2)

def gen_coathr_info():
	for aid in athr_full_info_dic.keys():
		athr_papers = athr_full_info_dic[aid]['pids']
		coathrs_set = set()

		for pid in athr_papers:
			coathrs_set = coathrs_set.union(paper_athr_list_dic[pid])

		athr_full_info_dic[aid]['co_aids'] = coathrs_set

def list_to_set(info_dic):
	new_info_dic = copy.copy(info_dic)

	for item_dic in info_dic.keys():
		for item_list in info_dic[item_dic].keys():
			if item_list == 'name': continue
			if item_list == 'is_cn': continue
			new_info_dic[item_dic][item_list] = set(info_dic[item_dic][item_list])
	
	return new_info_dic

def get_aids():
	global aids

	for aid in athr_basic_info_dic.keys():
		aids.append(aid)

def main():
	if len(sys.argv) < 5:
		print('Author.csv, Paper.csv, PaperAuthro.csv, CN_table, dump_file')
		exit(0)
	
	author_f_name = sys.argv[1]
	paper_f_name = sys.argv[2]
	paper_author_f_name = sys.argv[3]
	#dump_f_name_list = sys.argv[4] + '.list'
	cn_name_f_name = sys.argv[4]
	dump_f_name_set = sys.argv[5]

	print('Generating basic Paper Info')
	gen_paper_basic_info(paper_f_name)
	print('Generating basic Author Info')
	gen_athr_basic_info(author_f_name)
	print('Loading CN name id')
	gen_cn_name_index(cn_name_f_name)
	print('Generating Author Full Info')
	gen_athr_full_dic(paper_author_f_name)
	print('Generating Co-Author Info')
	gen_coathr_info()
	print('Get aids')
	get_aids()

#	cPickle.dump(athr_full_info_dic, open(dump_f_name, 'w'))
	#pickle.dump(athr_full_info_dic, open(dump_f_name_list, 'wb'))
	pickle.dump((list_to_set(athr_full_info_dic),aids), open(dump_f_name_set, 'wb'))

if __name__ == '__main__':
	main()
