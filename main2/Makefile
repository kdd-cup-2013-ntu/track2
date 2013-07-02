all:
	./gen_dedup_ids.py raw
	./predict_single.py raw_single.pkl > single.csv
	./collect_raw_name_v5.py raw_name_v5.pkl
	./raw_name_filter_v4.py raw_name_v5.pkl filtered_name_v54.pkl
	./abbr_extend_name_matching.py filtered_name_v54.pkl . v54
	./add_suffix.py filtered_name_v54.pkl suffix_dict_v54.pkl
	./chinese_name_grouping_v5.py suffix_dict_v54.pkl abbr_dict_v54.pkl extend_dict_v54.pkl group_dict_v54c4.pkl
	./gen_more_name_dict.py more_name_dict.pkl
	./name_authorId_pairing_v9.py more_name_dict.pkl name_id_v9.pkl
	./name_authorId_suffix.py suffix_dict_v54.pkl name_id_v9.pkl name_id_v9S.pkl
	./name2authorId_group.py group_dict_v54c4.pkl name_id_v9S.pkl N54c49S.csv
	cat single.csv > simplexN54c49S.csv
	cat N54c49S.csv >> simplexN54c49S.csv
	mv simplexN54c49S.csv ../buff/main2.csv -f

clean:
	rm *.pkl -f
	rm *.csv -f
	rm *.pyc -f
