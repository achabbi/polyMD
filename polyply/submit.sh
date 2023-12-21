#!/bin/bash

########### SBATCH TEMPLATE ###########
sbatch_type="SBATCH_ANALYSIS"

########### MOLECULE ###########
group="amide"
code="AMI"

########### LENGTH ###########
L0=40
Lf=200
L_inc=20

########### TEMPERATURE ###########
T0=673
Tf=673
T_inc=1

########### PRESSURE ###########
P0=1
Pf=1
P_inc=1

########### PATHS ###########
home="/project2/depablo/achabbi"
ff="/project2/depablo/achabbi/polyply/ff"
templates="/project2/depablo/achabbi/polyply/templates"
sbatch="/project2/depablo/achabbi/SBATCH_TEMPLATES"
GEN_GRO="/project2/depablo/achabbi/polyply/gen_gro.py"


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
#			rm LOG/*analysis.*
#			rm numbers.txt
#			rm SBATCH_ANALYSIS

			cd ../
		done
	done

	cd $home
	cd $group

done

