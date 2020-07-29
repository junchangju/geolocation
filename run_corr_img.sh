# outfile 

# Trying to get a pair of tie points from each file
outfile=tmp.all.tiepoint.txt

for dat in *[1-9].base.txt
do
	python ./corr_img.py $dat 

	# base=$(basename $dat .sam.base.txt)
	# corr=${base}.base.txt
	#python ./plotimg.py $corr 
done >$outfile

final=tmp.final.tiepoint.txt
grep final $outfile | awk '{print $2,$3,$4,$5}'  > $final

python ./arop_transform.py $final




