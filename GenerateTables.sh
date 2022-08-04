#!/bin/bash
#SBATCH -J s3mmp3mm   # A single job name for the array
#SBATCH -n 1            # Number of cores
#SBATCH -N 1            # All cores on one machine
#SBATCH -p guenette     # Partition
#SBATCH --mem 2000      # Memory request (Mb)
#SBATCH -t 0-8:00       # Maximum execution time (D-HH:MM)
#SBATCH -o /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC-tables/out/s3mmp3mm_%A.out
#SBATCH -e /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC-tables/err/s3mmp3mm_%A.err


## Configure scisoft software products
source /n/holystore01/LABS/guenette_lab/Lab/software/next/scisoft/setup #(already implemented in ~/.bashrc)
setup hdf5   v1_12_0b     -q e19:prof
setup geant4 v4_11_0_p01a -q e19:prof
setup cmake  v3_22_2
setup gsl    v2_7

module load python/3.8.5-fasrc01
unset PYTHONHOME
unset PYTHONPATH

cd /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC-tables/

# 1 hour and about 200 MB should be more than enough for GenerateSQLite3.py and GenerateTables.py
time python3 /n/holystore01/LABS/guenette_lab/Lab/data/NEXT/FLEX/mc/eres_22072022/IC-tables/GenerateTables.py
