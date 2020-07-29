# Try to code a bit on registration to understand it more.


. ~/toa.code/L8/driver_script/setenv.sh local
export TDIR=$dir/jju/tmpdir
export ACCODE=TOA_data

# for pr in 015033 015034
# do
# 	~/toa.code/L8/copyL8L1/script/copyL8L1_onepr.sh $pr 2019-05-24 2019-05-24 
# 	~/toa.code/L8/copyL8L1/script/copyL8L1_onepr.sh $pr 2019-07-27 2019-07-27 
# 	~/toa.code/L8/copyL8L1/script/copyL8L1_onepr.sh $pr 2019-12-18 2019-12-18
# done

for scene in $(ls -d $dir/jju/L8L1/*/*/*/*)
do
	:
	# echo $scene
	# $CODE_BASE_DIR/L8/angle/angle_scene/script/run_angle_scene.sh $scene
	# ~/toa.code/L8/toTOA/script/run_toa.sh $scene
done

# aws s3 cp s3://hlsanc/S2REFIMG/18SUH.2016.6.20.0.S2A_B08.bin $TDIR
# aws s3 cp s3://hlsanc/S2REFIMG/18SUH.2016.6.20.0.S2A_B08.hdr $TDIR
s2refimg=$TDIR/18SUH.2016.6.20.0.S2A_B08.bin
refimghdr=$TDIR/18SUH.2016.6.20.0.S2A_B08.hdr
set $(awk -F"," '$0 ~ /map info/ {print $4, $5}' $refimghdr )
sulx=$1
suly=$2

outfile=tmp.corr.txt
for landsat in $(ls $LOCAL_IO_DIR/L8/SR/SR_SCENE/*/*/*/*hdf)
do
	bname=$(basename $landsat .hdf)
	l8bin=$TDIR/${bname}.bin
	# echo $l8bin

	set $(awk '$1 == "samples" {ncol = $3}
		   $1 == "lines"   {nrow = $3}
		   END {print nrow, ncol}' $landsat.hdr)
	nrow=$1
	ncol=$2

	set $(awk -F"," '$0 ~ /map info/ { print $4, $5}' $landsat.hdr)
	lulx=$1
	luly=$2

	# hdp dumpsds -n band05 -b -o $l8bin  $landsat

	# ./match $s2refimg $sulx $suly $l8bin $lulx $luly $nrow $ncol  2>$outfile

	break
done

N=$( sort -n -k1,1 $outfile | tail -1 | awk '{print $1}' )

for i in $(seq 1 $N)
do
	awk -v id=$i '
		BEGIN { SD = 15; winsz = SD*2 + 1;
			for (i = 0; i < winsz; i++)
				for (j = 0; j < winsz; j++)
					corr[i][j] = -1
		      }
		$1 == id { corr[$2-$4 + SD][$3-$5 + SD] = $NF }
	        END { 	for (i = 0; i < winsz; i++) {
				for (j = 0; j < winsz; j++) 
			 		printf("%lf ", corr[i][j]);
				printf("\n")
			}
		     } ' $outfile > ${i}.base.txt

done

