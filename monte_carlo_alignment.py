################################################################################
# python script for structure alignment using Monte Carlo method               #
# Author: Panyue Wang                                                          #
# Email: pywang@ucdavis.edu                                                    #
# Usage: python monte_carlo_alignment.py input_pdb target_pdb output_pdb       #
################################################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import sys

# returns CA and all atom coordinates
def pdb_parser(pdb_file_obj):
    ca_coords = []
    atom_coords = []
    for line in pdb_file_obj:
        xyz = np.zeros(3)
        line_arr = line.split()
        if line_arr[0] == "TER":
            break
        xyz[0] = float(line_arr[6])
        xyz[1] = float(line_arr[7])
        xyz[2] = float(line_arr[8])
        # get C-alphas
        if line_arr[2] == "CA":
            ca_coords.append(xyz)
        atom_coords.append(xyz)
    
    return np.array(ca_coords), np.array(atom_coords)

def coord_to_str(coord):
    string = "{:.3f}".format(coord[0]) + " " + "{:.3f}".format(coord[1]) +\
         " " + "{:.3f}".format(coord[2])

    return string

# output to pdb
def write_to_pdb(input_pdb_obj, aligned_coords, output_pdb_obj):
    for coord in aligned_coords:
        line = input_pdb_obj.readline()
        # convert new coords to str
        aligned_coord_str = coord_to_str(coord) 
        # replace input coords with new coords
        rep_line = line.replace(line[32:54], aligned_coord_str)
        # write to output
        output_pdb_obj.write(rep_line)
    output_pdb_obj.write("TER\n")
    output_pdb_obj.write("END\n")

# calculate the RMSD between the target and the input
def get_RMSD(target, input):
    atom_count = target.shape[0]
    target_flat = target.reshape([atom_count*3, 1])
    input_flat = input.reshape([atom_count*3, 1])
    delta = target_flat - input_flat
    delta = np.square(delta)
    delta_mean = np.sum(delta) / atom_count
    RMSD = np.sqrt(delta_mean)

    return RMSD

# calculate center of mass
def get_com(coords):
    com = np.mean(coords, axis=0)
    return com

# Monte Carlo functions
def MC_translation(stepsize):
    translation_vec = np.random.randn(3) * stepsize

    return translation_vec

def MC_rotation(com, stepsize):
    # around Z
    rotation_angle = np.cos(np.pi / 8) #np.random.randn() * stepsize
    rotation_vec = com #np.random.randn(3) - com
    rotation_quat = np.append(rotation_vec, rotation_angle)
    # rotation operations
    r = R.from_quat(rotation_quat)

    return r

def MC_alignment(target_ca_arr, input_ca_arr, input_coord_arr, \
    steps, stepsize, tol):
    # RMSD array for plotting
    RMSD_arr = []
    # initial RMSD
    RMSD_i = get_RMSD(target_ca_arr, input_ca_arr)
    for i in range(steps):
        # propose a random move
        tr_vec = MC_translation(stepsize)
        input_ca_arr += tr_vec
        RMSD = get_RMSD(target_ca_arr, input_ca_arr)
        # if RMSD is decreasing
        if RMSD < RMSD_i:
            # accept the move
            input_coord_arr += tr_vec
            # update limit
            RMSD_i = RMSD
            # check convergence
            if RMSD < tol:
                RMSD_arr.append(RMSD_i)
                break
        else:
            # adaptive step size
            if RMSD < 1:
                stepsize *= 0.8
            # reject the move
            input_ca_arr -= tr_vec
        RMSD_arr.append(RMSD_i)

    return input_coord_arr, np.array(RMSD_arr)

if __name__ == "__main__":
    # getting inputs
    input_pdb = open(sys.argv[1], 'r')
    input_ca, input_atom = pdb_parser(input_pdb)
    target_pdb = open(sys.argv[2], 'r')
    # output
    output_pdb = open(sys.argv[3], 'w')
    target_ca, target_atom = pdb_parser(target_pdb)
    # Monte Carlo alignment
    steps = 10000
    stepsize = 2
    tol = 0.1
    input_aligned, RMSD = MC_alignment(target_ca, input_ca, input_atom,steps, stepsize, tol)
    # plotting RMSD
    plt.figure()
    plt.title("RMSD vs steps")
    plt.xlabel("steps")
    plt.ylabel("RMSD [Å]")
    plt.plot(RMSD, '-o')
    plt.show()
    # output the aligned structure to pdb
    input_pdb.seek(0)
    write_to_pdb(input_pdb, input_aligned, output_pdb)

    #com = get_com(input_atom)
    #rot = MC_rotation(com, 0)
    #input_rot = []
    #for atom in input_atom:
    #    input_rot.append(rot.apply(atom))
    
    #input_rot = np.array(input_rot)
    pass