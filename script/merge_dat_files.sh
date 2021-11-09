PREFIX=$1
START=$2
FINISH=$3
OUTPUT=$4

echo "Merging files with PREFIX $PREFIX$START to $PREFIX$FINISH"

for f in $(seq $START $FINISH); 
do
  FILE="$PREFIX$f.dat"
  echo "Merging file : $FILE"
  if [ $f -eq $START ]
  then
      tail -n +2 $FILE > $OUTPUT
  else
    tail -n +2 $FILE >> $OUTPUT
  fi
  
  
done

