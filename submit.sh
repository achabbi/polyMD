#!/bin/bash

########### SBATCH TEMPLATE ###########
sbatch_type="SBATCH_MIDWAY2"

########### MOLECULE ###########
group="urethane"
code="URE"

########### LENGTH ###########
L0=40
Lf=200
L_inc=20

########### TEMPERATURE ###########
T0=373
Tf=573
T_inc=100

########### PRESSURE ###########
P0=1
Pf=1
P_inc=1

########### TIME ###########
TIME_NPT=10
TIME_NVT=100

########### PATHS ###########
home="/project2/depablo/achabbi/molecules"
sbatch="/project2/depablo/achabbi/SBATCH_TEMPLATES"


########### MAIN ###########
cd $home
cd $group

for L in $(seq $L0 $L_inc $Lf)
do
	cd $code$L

	for T in $(seq $T0 $T_inc $Tf)
	do
		for P in $(seq $P0 $P_inc $Pf)
		do
			cd T${T}_P${P}
			sbatch ${sbatch_type}
			cd ../
		done
	done

	cd $home
	cd $group

done
