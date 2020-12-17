################################################################################
# python script for structure alignment using Monte Carlo method               #
# Author: Panyue Wang                                                          #
# Email: pywang@ucdavis.edu                                                    #
################################################################################
import numpy as np
import matplotlib.pyplot as plt
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
    string = str(coord[0]) + " " + str(coord[1]) + " " + str(coord[2])
    return string

# output to pdb
def write_to_pdb(input_pdb_obj, aligned_coords, output_pdb_obj):
    for coord in aligned_coords:
        line = input_pdb_obj.readline()
        # convert new coords to str
        aligned_coord_str = coord_to_str(coord) 
        # replace input coords with new coords
        line.replace(line[32:54], aligned_coord_str)
        # write to output
        output_pdb_obj.write(line)
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
    translation_vec = np.zeros(3)
    translation_vec = np.random.randn(3) * stepsize
    #translation_vec[1] = np.random.randn() * stepsize
    #translation_vec[2] = np.random.randn() * stepsize

    return translation_vec

def MC_rotation(com, stepsize):
    rotation_vec = np.zeros(3)
    rotation_vec= np.random.randn(3) 
    #rotation_vec[1] = np.random.randn(3) 
    #rotation_vec[2] = np.random.randn(3) 
    pass

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
    stepsize = 3
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
    #input_pdb.seek(0)
    #write_to_pdb(input_pdb, input_aligned, output_pdb)

    pass