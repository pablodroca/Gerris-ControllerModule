#! /bin/bash
./clear_results.sh
mkdir -p results
time gerris2D -m cylinder_control.gfs 2>log.txt
