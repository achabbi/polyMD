# polyMD

Moleculer dynamics pipeline for running high-throughput simulations on cleavable-bond modified polyethylene. Designed for SLURM-based HPC clusters. This uses the [GROMACS](https://www.gromacs.org/) MD simulation software with the OPLS united-atom forcefield.

## Setup

1. Clone repository.

```sh
git clone https://github.com/achabbi/polyMD.git
cd polyMD/
```

2. Create conda environment.

```sh
module load python
conda env create --prefix=/path/to/new/environment -f environment.yml
source activate polyMD
```

## Usage

### File Structure

[`molecules/`](molecules/) contains all simulation files for each molecule type, with the **amide** group shown below:

```bash
.
├── molecules
│   ├── amide                             # files for amide functional group
│   │   ├── AMI100                        # 100 carbons length
│   │   │   ├── T473_P1                   # NPT and NVT runs at 473 K and 1 bar
│   │   │   │   ├── LOG                   # log files
│   │   │   │   │   └── ...
│   │   │   │   ├── MDP                   # mdp files
│   │   │   │   │   ├── anneal.mdp
│   │   │   │   │   ├── condense.mdp
│   │   │   │   │   ├── minimize.mdp
│   │   │   │   │   ├── npt.mdp
│   │   │   │   │   └── nvt.mdp
│   │   │   │   ├── SBATCH_ANALYSIS       # SBATCH script for running analysis
│   │   │   │   ├── SBATCH_MIDWAY2        # SBATCH script for running simulations
│   │   │   │   ├── condense              # files after condensation run
│   │   │   │   │   └── condense.gro
│   │   │   │   ├── em                    # files after energy minimization run
│   │   │   │   │   └── em.gro
│   │   │   │   ├── npt                   # files after NPT run
│   │   │   │   │   ├── density.xvg
│   │   │   │   │   └── npt.gro
│   │   │   │   ├── numbers.txt           # properties computed from analysis
│   │   │   │   └── nvt                   # files after NVT run
│   │   │   │       ├── conformation.xvg
│   │   │   │       ├── msd.xvg
│   │   │   │       └── nvt.gro
│   │   │   └── TOP                       # topology files
│   │   │       ├── AMI.gro               # starting coords (100 molecules)
│   │   │       ├── AMI.itp               # bonded forcefield params
│   │   │       ├── AMI_original.gro      # starting coords (1 molecule)
│   │   │       └── OPLS_AMI.top
│   │   ├── ffnonbonded.itp               # non-bonded forcefield params
│   │   ├── forcefield.itp
│   │   └── top_template.top
│   ├── aromatic_ester                    # files for aromatic ester
│   │   └── ...
│   ├── carbonate                         # files for carbonate
│   │   └── ...
│   ├── ester                             # files for ester
│   │   └── ...
│   ├── polyethylene                      # files for polyethylene
│   │   └── ...
│   └── urethane                          # files for urethane
│       └── ...
└── ...
```

All files generated at each step (energy minimization, condensation, NPT, NVT) are stored in their respective folders for each molecule type and configuration (i.e., AMI100 at T473_P1). The primary scripts for running simulation and analysis jobs are [`setup_runs.sh`](setup_runs.sh), [`setup_analysis.sh`](setup_analysis.sh), and [`submit.sh`](submit.sh), explained in the next section.

### Running Simulations

To setup and submit simulation jobs, edit the parameters in [`setup_runs.sh`](setup_runs.sh) and [`submit.sh`](submit.sh) to be the same, then run both scripts.

- Select/edit either [`SBATCH_MIDWAY3`](SBATCH_TEMPLATES/SBATCH_MIDWAY3) or [`SBATCH_MIDWAY2`](SBATCH_TEMPLATES/SBATCH_MIDWAY2) files from [`SBATCH_TEMPLATES/`](SBATCH_TEMPLATES/)
- Set `sbatch_type="SBATCH_MIDWAY3"` or `sbatch_type="SBATCH_MIDWAY2"` in both shell scripts

```sh
cd polyply/
bash setup_runs.sh
bash submit.sh
```

### Running Analysis

To setup and submit analysis jobs on simulation trajectories, edit the parameters in [`setup_analysis.sh`](setup_analysis.sh) and [`submit.sh`](submit.sh) to be the same, then run both scripts.

- Edit [`SBATCH_ANALYSIS`](SBATCH_TEMPLATES/SBATCH_ANLAYSIS) from [`SBATCH_TEMPLATES/`](SBATCH_TEMPLATES/)
- Set `sbatch_type="SBATCH_ANALYSIS"` in both shell scripts

```sh
cd polyply/
bash setup_analysis.sh
bash submit.sh
```

Run [`compile.py`](scripts/compile.py) to compile results into a single csv for the desired molecule. If the csv file already exists in [`csv_files/`](csv_files/), it will be updated with the new data. Otherwise, a new csv file will be created.

```sh
# Running for ester group (EST)
python compile.py -c EST
```

## License and Acknowledgements

Copyright (c) 2023 Archit Chabbi, María Ley Flores. This research was performed at the de Pablo group at the University of Chicago. Resources were provided by the University of Chicago Research Computing Center.
