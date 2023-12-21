#!/bin/bash

########### SBATCH TEMPLATE ###########
sbatch_type="SBATCH_MIDWAY2"

########### MOLECULE ###########
group="urethane"
code="URE"

########### LENGTH ###########
L0=40
Lf=200
L_inc=1

########### TEMPERATURE ###########
T0=373
Tf=573
T_inc=1

########### PRESSURE ###########
P0=1
Pf=1
P_inc=1

########### TIME ###########
TIME_NPT=10
TIME_NVT=100

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
	mkdir -p $code$L
	cd $code$L
	mkdir -p TOP
	cd TOP
	
	if [ ! -e "${code}.itp" ]; then
		PE=$(($L/4))
		echo "Generating $code.itp"
		polyply gen_params -f $ff/$group.ff -name $code -seq CH3ter:1 PE:$PE $code:1 PE:$PE CH3ter:1 -o $code.itp
	fi

	if [ ! -e "${code}_original.gro" ]; then
		python $GEN_GRO $templates/${code}_template.gro ${code}_original.gro $L $code
	fi

	if [ ! -e "OPLS_${code}.top" ]; then
		cp $home/$group/top_template.top OPLS_${code}.top
	fi	

	cd ../

	for T in $(seq $T0 $T_inc $Tf)
	do
		for P in $(seq $P0 $P_inc $Pf)
		do
			mkdir -p T${T}_P${P}
			cd T${T}_P${P}

			mkdir -p LOG
			cp ${sbatch}/${sbatch_type} ./

			sed -i "s/NAME2/${code}${L}_T${T}_P${P}/g" "${sbatch_type}"
			sed -i "s/CODE2/${code}/g" "${sbatch_type}"
			sed -i "s/TEMP2/${T}/g" "${sbatch_type}"
			sed -i "s/PRES2/${P}/g" "${sbatch_type}"
			sed -i "s/TIMENPT2/${TIME_NPT}/g" "${sbatch_type}"
			sed -i "s/TIMENVT2/${TIME_NVT}/g" "${sbatch_type}"

			cd ../
		done
	done

	cd $home
	cd $group

done

