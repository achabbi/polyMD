# polyMD

Moleculer dynamics pipeline for running high-throughput simulations on cleavable-bond modified polyethylene. Designed for SLURM-based computing clusters. This uses the [GROMACS](https://www.gromacs.org/) MD simulation software with the OPLS united-atom forcefield.

## Setup

1. Clone repository

```shell
$ git clone
$ cd polyMD/
```

2. Create conda environment

```shell
$ module load python
$ conda env create --prefix=/path/to/new/environment -f environment.yml
$ source activate polyMD
```

## Usage

### Running Simulations

To setup and submit simulation jobs, edit the parameters in `polyply/setup_runs.sh` and `polyply/submit.sh` to be the same, then run both scripts.

- Select/edit either `SBATCH_MIDWAY3` or `SBATCH_MIDWAY2` files from `SBATCH_TEMPLATES/`
- Set `sbatch_type="SBATCH_MIDWAY3"` or `sbatch_type="SBATCH_MIDWAY2"` in both shell scripts

```shell
$ cd polyply/
$ bash setup_runs.sh
$ bash submit.sh
```

### Running Analysis

To setup and submit analysis jobs on simulation trajectories, edit the parameters in `polyply/setup_analysis.sh` and `polyply/submit.sh` to be the same, then run both scripts.

- Edit `SBATCH_ANALYSIS` file from `SBATCH_TEMPLATES/`
- Set `sbatch_type="SBATCH_ANALYSIS"` in both shell scripts

```shell
$ cd polyply/
$ bash setup_analysis.sh
$ bash submit.sh
```

Run `compile.py` to compile results into a single csv for the desired molecule. If the csv file already exists in `csv_files/`, it will be updated with the new data. Otherwise, the file will be created under `csv_files/`.

```shell
# Running for ester group (EST)
python compile.py -c EST
```

## License

Copyright (c) 2023 Archit Chabbi, María Ley Flores.
