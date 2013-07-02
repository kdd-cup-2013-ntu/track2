RAWFILE:="dataRev2.zip"
FAKEDIR:="fake"

all: final.csv

final.csv: data buff buff/typo.csv buff/main1.csv buff/main2.csv
	make -C merge

buff/typo.csv: buff data
	make -C typo
	#ln -sf ../$(FAKEDIR)/typo.csv buff/typo.csv

buff/main1.csv: buff data
	make -C main1
	#ln -sf ../$(FAKEDIR)/dijkstra_0612_1.csv buff/main1.csv

buff/main2.csv: buff data
	make -C main2
	#ln -sf ../$(FAKEDIR)/simplexN54c49S.csv buff/main2.csv

buff:
	mkdir -p buff

data:
	mkdir -p data
	unzip $(RAWFILE) -d data
	chmod -w data/*

clean:
	make -C merge clean
	make -C main1 cleanclean
	make -C main2 clean
	make -C typo clean
	rm -rf buff data final.csv
