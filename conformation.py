import sys
import numpy as np


def conformation(file):
    data = np.genfromtxt([i for i in open(file).read().splitlines() if not i.startswith(('#','@'))])
    x = data[:, 0]/1000
    ee = data[:, 1]
    rg = data[:, 2]

    section_size = len(x) // 5
    ee_sections = [ee[i:i + section_size] for i in range(0, len(ee), section_size)]
    rg_sections = [rg[i:i + section_size] for i in range(0, len(rg), section_size)]

    ee_averages = [np.mean(section) for section in ee_sections]
    rg_averages = [np.mean(section) for section in rg_sections]

    ee_overall = np.mean(ee_averages)
    rg_overall = np.mean(rg_averages)

    ee_error = np.std(ee_averages)
    rg_error = np.std(rg_averages)

    return ee_overall, ee_error, rg_overall, rg_error


conf_file = str(sys.argv[1])
numbers_file = str(sys.argv[2])

ee_overall, ee_error, rg_overall, rg_error = conformation(conf_file)

with open(numbers_file, 'a') as file:
    file.write(f'{ee_overall} {ee_error}\n')
    file.write(f'{rg_overall} {rg_error}\n')


