#O1
cd O1
mpirun -np 8 mms2d mms2d.prm
cp L2Error-2D.dat ../O1.dat
cd ..
python3  ../../python/mms/plotL2Error.py  O1.dat
cp L2Error.png O1.png

#O2
cd O2
mpirun -np 8 mms2d mms2d.prm
cp L2Error-2D.dat ../O2.dat
cd ..
python3  ../../python/mms/plotL2Error.py  O2.dat
cp L2Error.png O2.png
sleep 3

#O3
cd O3
mpirun -np 8 mms2d mms2d.prm
cp L2Error-2D.dat ../O3.dat
cd ..
python3  ../../python/mms/plotL2Error.py  O3.dat
cp L2Error.png O3.png
sleep 3

#O4
cd O4
mpirun -np 8 mms2d mms2d.prm
cp L2Error-2D.dat ../O4.dat
cd ..
python3  ../../python/mms/plotL2Error.py  O4.dat
cp L2Error.png O4.png
sleep 3




