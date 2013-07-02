CH="information"

ln -s -T ../../data/Author.csv Author.csv

echo "Split Author.csv..."
perl split_author.pl Author.csv

echo "Start to detect chinese..."
perl show_chinese.pl Author.csv.aid Author.csv.name ${CH}/last.all ${CH}/token.all ${CH}/last.ban ${CH}/token.ban|perl show_p.pl > ../../buff/chinese_author.less
