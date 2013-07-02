mkdir tmpdata
echo 1 generate word frequency
./lg_name_a.py ../data/PaperAuthor.csv ../data/Author.csv
echo 2 sort frequency file
sort -n --key=2 tmpdata/a.count > tmpdata/a.count.sort
echo 3 group words according to frequency
python split.py
echo 4 get typo list
python similar.py
echo 5 select more confident ones and generate csv file
./2stage.py
mv typo.csv ../buff
