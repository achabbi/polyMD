import sys
import math
import numpy as np
from scipy.optimize import fsolve


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))

    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)

    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d

    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])



def equations(p, p0, p00, p000, theta):
    new_v1 = p00 - p0
    new_v2 = p000 - p00
    x, y, z = p

    n = np.cross(-new_v1, new_v2)
    a, b, c = np.dot(rotation_matrix(-new_v1, theta), n)
    d = np.dot(n, p0)

    eq1 = a*x + b*y + c*z - d # plane, constant
    eq2 = (x - p0[0])**2 + (y - p0[1])**2 + (z - p0[2])**2 - bond_length**2 # distance, loop
    eq3 = ((x - p0[0])*(new_v1[0])) + ((y - p0[1])*(new_v1[1])) + ((z - p0[2])*(new_v1[2])) - k # angle, loop

    return (eq1, eq2, eq3)


# define inputs
original_name = str(sys.argv[1]) # template file
new_name = str(sys.argv[2]) # output file
ncarbs = int(sys.argv[3]) # number of carbons total
mol = str(sys.argv[4]) # molecule code (EST)


# run script
print(f"Generating {new_name}")

original = open(original_name, 'r')
new = open(new_name, 'w')

begin = True
start_atom_num = 110

lines = original.readlines()
carbons = int((ncarbs/2) - 2 + 1)

new.write(mol + '\n')
new.write('    ' + str(int(2*carbons + len(lines))) + '\n')


for idx in range(2):
    x = 0
    y = 0
    z = 0

    points = []
    group = []

    i = 0
    start = 2

    if begin:
        for line in lines:
            if i == 3:
                break
            if mol not in line:
                continue
            vals = [x for x in line.split(' ') if x != '']
            x = float(vals[3]) # this is the first point
            y = float(vals[4])
            z = float(vals[5])

            points.append(np.array([x, y, z]))
            i += 1
    else:
        lines.reverse()
        for line in lines:
            if mol not in line:
                continue
            vals = [x for x in line.split(' ') if x != '']
            x = float(vals[3])
            y = float(vals[4])
            z = float(vals[5])
            
            points.append(np.array([x, y, z]))
            i += 1
            if i == 3:
                break

    group_old = [line for line in lines if mol in line]
    for line in group_old[3:-3]:
        vals = [x for x in line.split(' ') if x != '']
        x = float(vals[3])
        y = float(vals[4])
        z = float(vals[5])
        group.append(np.array([x, y, z]))

    v1 = points[0] - points[1] # vector away from molecule
    v2 = points[2] - points[1]

    angle = (2*np.pi)/3 # 120 degrees
    bond_length = 0.152
    mag_v1 = np.linalg.norm(v1)
    k = np.cos(angle)*bond_length*mag_v1



    atoms = []
    atom_nums = []
    coords = []

    p0 = points[0]
    p00 = points[1]
    p000 = points[2]

    theta = 0

    for i in range(carbons):
        if begin:
            atom = f"CO{start}"

            init_guess = np.array((p0[0]+0.02, p0[1]+0.02, p0[2]+0.02))
            x, y, z = fsolve(equations, init_guess, args=(p0, p00, p000, theta))

            atoms.insert(0, atom)
            atom_nums.insert(0, carbons-i)
            coords.insert(0, (f'{x:.3f}', f'{y:.3f}', f'{z:.3f}'))
            start = (start % 2) + 1
        else:
            start = (start % 2) + 1
            atom = f"CO{start}"

            init_guess = np.array((p0[0]+0.02, p0[1]+0.02, p0[2]+0.02))
            x, y, z = fsolve(equations, init_guess, args=(p0, p00, p000, theta))

            atoms.append(atom)
            atom_nums.append(start_atom_num + i)
            coords.append((f'{x:.3f}', f'{y:.3f}', f'{z:.3f}'))

        p000 = p00
        p00 = p0
        p0 = np.array((x, y, z))



    for i in range(len(atoms)):
        x = coords[i][0]
        y = coords[i][1]
        z = coords[i][2]

        if (idx == 0 and i == 0) or (idx == 1 and i == (len(atoms) - 1)):
            atoms[i] = 'CT1'

        line = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f" % (1, mol, atoms[i], int(atom_nums[i]), float(x), float(y), float(z))
        new.write(line + '\n')

    if idx == 0:
        for k in range(len(lines)):
            nums = lines[k].split()
            nums[2] = str(int(atom_nums[-1]) + k + 1)

            x = nums[3]
            y = nums[4]
            z = nums[5]

            line = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f" % (1, nums[0], nums[1], int(nums[2]), float(x), float(y), float(z))
            new.write(line + '\n')

        start_atom_num = len(atom_nums) + len(lines) + 1
    begin = False


new.write('   20.00000   20.00000   20.00000\n')

original.close()
new.close()

print('DONE')