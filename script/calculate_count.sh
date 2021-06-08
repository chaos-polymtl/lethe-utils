#!/bin/bash

# Change this path to get .prm files
for f in /home/audrey/work/lethe/lethe/examples/rpt/count_calculation/*.prm; do
	echo $f; # Show the current file
	# Change this path to use the rpt_3d application
	/home/audrey/work/lethe/build/applications/rpt_3d/rpt_3d "$f"
done