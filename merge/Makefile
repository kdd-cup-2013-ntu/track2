all: final.csv

final.csv: buff tools buff/elite.csv buff/typo.csv buff/main1.csv
	tools/scripts/mergecsv2.py tools/data_local/Author.csv buff/main1.csv buff/elite.csv buff/main1_merge.csv
	tools/scripts/mergecsv.py buff/main1_merge.csv buff/typo.csv final.csv
	cp final.csv ..

buff/elite.csv: buff/AffilList2.csv buff/Paper.TitleCut.csv buff/Paper.TitleStat.csv buff/main1.csv buff/main2.csv
	./diff2.py

buff/Paper.TitleCut.csv: buff/Paper.TitleStat.csv data/Paper.csv
	./StringToWord.py

buff/Paper.TitleStat.csv: data/Paper.csv
	./Statistic.py

buff/AffilList2.csv: buff/PA_speci.csv
	./Affiliation2.py

buff/PA_speci.csv: buff/PAtoAa.csv
	./Name_combine.py

buff/PAtoAa.csv: data
	./PAtoA.py	

buff/main1.csv:
	ln -sf ../../buff/main1.csv buff/main1.csv

buff/main2.csv:
	ln -sf ../../buff/main2.csv buff/main2.csv

buff/typo.csv:
	ln -sf ../../buff/typo.csv buff/typo.csv

tools: data
	mkdir -p tools/data_local
	ln -sf ../../main1/main/kdd tools/kdd
	ln -sf ../../main1/main/scripts tools/scripts
	cp data/Author.csv tools/data_local
	chmod +w tools/data_local/*
	tools/scripts/rmheader.sh tools/data_local/Author.csv

data:
	ln -s ../data

buff:
	mkdir buff

clean:
	rm -rf buff data ./*.pyc tools final.csv
