import os
import re
import glob
import pandas as pd
import argparse


groups = {
    'EST': 'ester',
    'ARO': 'aromatic_ester',
    'ANH': 'anhydride',
    'CAR': 'carbonate',
    'URE': 'urethane',
    'AMI': 'amide'
}

parser = argparse.ArgumentParser(description='Compile data from numbers.txt files')
parser.add_argument('-c', '--code', type=str, required=True, help='Group code')
args = parser.parse_args()

code = args.code
group = groups[code]

try:
    df = pd.read_csv(f'csv_files/{group}_data.csv')
except:
    df = pd.DataFrame(columns=['carbons', 
                               'temperature', 
                               'pressure', 
                               'density', 'density_error', 
                               'diff', 'diff_error', 
                               'ee', 'ee_error', 
                               'rg', 'rg_error'])

wd = os.getcwd()

for path in glob.glob(f'{wd}/{group}/{code}*/T*_P*/numbers.txt'):
    
    with open(path, 'r') as file:
        lines = [line.strip() for line in file.readlines() if not line.isspace()]
    
    if len(lines) != 4:
        print(path)
        continue

    c_pattern = rf'{code}(\d+)'
    c_match = re.search(c_pattern, path)
    carbons = c_match.group(1)

    t_pattern = r'T(\d+)_'
    t_match = re.search(t_pattern, path)
    temp = t_match.group(1)

    p_pattern = r'_P(\d+)'
    p_match = re.search(p_pattern, path)
    pressure = p_match.group(1)

    is_duplicate = df.loc[(df['carbons'] == int(carbons)) & 
                          (df['temperature'] == int(temp)) & 
                          (df['pressure'] == int(pressure))].any().all()
    
    if not is_duplicate:
        filename = os.path.basename(path)

        values = [float(line.split(' ')[0]) for line in lines]
        errors = [float(line.split(' ')[1]) for line in lines]
        
        new_row = {
            'carbons': carbons,
            'temperature': temp,
            'pressure': pressure,

            'density': values[0],
            'density_error': errors[0],

            'diff': values[1],
            'diff_error': errors[1],

            'ee': f'{values[2]:.4f}',
            'ee_error': f'{errors[2]:.4f}',

            'rg': f'{values[3]:.4f}',
            'rg_error': f'{errors[3]:.4f}'
        }

        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        print(f'{code}: Added C = {carbons}, T = {temp}, P = {pressure}')


df.to_csv(f'csv_files/{group}_data.csv', index=False)