To launch all the simulations
for i in $(ls hopper_*.sh); do sbatch $i; done

To gather all the timing results
for i in $(ls *.out); echo $i ; do grep "Total wall" $i | tail -1 | cut -c 50- | cut -c -10; done