solver=$1
nproc=$2

declare -a arr=("O1" "O2" "O3" "O4")

for i in "${arr[@]}"
do
    echo "Running case : $i"
    cd $i
    mpirun -np $nproc $solver mms2d.prm
    cp L2Error.dat ../"$i.dat"
    cd ..
    python3  ../../python/mms/plotL2Error.py  "$i.dat"
    cp L2Error.png "$i.png"
    sleep 3
done

python3 ../../python/mms/plotErrorTime.py  O1.dat O2.dat O3.dat O4.dat

