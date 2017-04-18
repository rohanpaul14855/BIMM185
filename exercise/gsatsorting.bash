#!/bin/bash

#The following script gets the highest GSAT score from each
#report.tbl file. The filename and the score are then sorted
#in descending order of the score then by name

for i in $(ls); do
	gsat=$(head -3 $i/$i/report.tbl | tail -1 | cut -f4)
	echo $i    $gsat >> gsat.txt
	sed -e 's/ /	/g' gsat.txt | sort -k2nr -k1 >> sortedgsat.txt
done
